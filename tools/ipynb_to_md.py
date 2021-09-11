import argparse
import base64
import datetime
import io
import json
import os
from typing import Union

import pandas as pd
from PIL import Image

HelpMSG = ''''''


def init_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=HelpMSG)
    # work folder
    parser.add_argument('-ipynb', '--ipynb_file', metavar='path', type=str, default=None, required=True,
                        help='')
    parser.add_argument('-mddir', '--md_dir', metavar='path', type=str, default=None, required=True,
                        help='')
    parser.add_argument('-mdname', '--md_filename', metavar='name', type=str, default=None, required=False,
                        help='')
    parser.add_argument('-img', '--img_folder', metavar='path', type=str, default=None, required=False,
                        help='')
    parser.add_argument('-skiptitle', '--skip_1st_title', metavar='int', type=int, default=1, required=False,
                        help='')
    parser.add_argument('-overwrite', '--overwrite_confirm', metavar='int', type=int, default=1, choices=[0, 1], required=False,
                        help='')
    parser.add_argument('-title', '--markdown_title', metavar='[str|int]', type=Union[str, int], default=1, required=False,
                        help='0 with no title, 1 with default title (Date: 20xx-xx-xx\\nFile name: DATE-xxx.md), or define a title in string')
    return parser


def load_ipynb_cells(path, skip_1st_title=None):
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    cells = content.get('cells')
    if cells is None:
        raise ValueError(f'Key `cells` is not in current file: {path}')
    if skip_1st_title is not None:
        if not isinstance(skip_1st_title, int):
            raise ValueError(f'`skip_1st_title` must has a int value if not `None`, now {skip_1st_title}')
        if skip_1st_title == 0:
            pass
        else:
            count_1st_title = 0
            for i, d in enumerate(cells):
                if d['cell_type'] == 'markdown' and d['source'][0].lstrip(' ').startswith('# '):
                    if count_1st_title == skip_1st_title:
                        cells = cells[i:]
                        break
                    count_1st_title += 1
    return cells


def parse_ipynb_cells(cells):
    text = []

    for cell_idx, cell in enumerate(cells, 1):
        cell_type = cell['cell_type']
        cell_source = cell['source']
        if cell_type == 'markdown':
            text.append([cell_idx, 'text', None, cell_source])
        elif cell_type == 'code':
            if not cell_source:
                continue
            cell_outputs = cell.get('outputs')
            if cell_outputs is None or not cell_outputs:
                continue

            for output_idx, output in enumerate(cell_outputs):
                output_data = output.get('data')
                if output_data is None:
                    text.append([cell_idx, 'code', None, output.get('text')])
                else:
                    if 'text/html' in output_data:
                        html_text = ''.join(output_data['text/html'])
                        if '.dataframe' in html_text:
                            df = pd.read_html(html_text)[0]
                            df = df.set_index(df.columns[0])
                            df.index.rename('idx', inplace=True)
                            text.append([cell_idx, 'text', None, df.to_markdown()])
                    elif 'image/png' in output_data:
                        text.append([cell_idx, 'img', None, output_data.get('image/png')])
                    elif 'text/plain' in output_data:
                        text.append([cell_idx, 'code', None, output_data.get('text/plain')])
                    else:
                        print(f'Cell idx: {cell_idx} with no suitable output type')
        else:
            print(f'Cell idx: {cell_idx} is not `markdown` or `code`')

    return text


def write_md_title(f, title, md_filename):
    if title == 0:
        return
    elif title == 1:
        if md_filename[:8].isdigit():
            md_title_date = f'{md_filename[:4]}-{md_filename[4:6]}-{md_filename[6:8]}'
        else:
            md_title_date = datetime.datetime.now().strftime("%Y-%m-%d")
        f.write(f'Date: {md_title_date}\n\n')
        f.write(f'File name: {md_filename}\n\n')
    elif isinstance(title, str):
        pass
    else:
        raise ValueError(f'MarkDown title should be 0 (no title), 1 (default title), or defined string. Now {title}')


def write_one_item(f, content, cell_idx):
    if isinstance(content, str):
        content = [content]
    if isinstance(content, (list, tuple)):
        for c in content:
            f.write(c)
        f.write('\n')
    else:
        raise ValueError(f'[Cell idx {cell_idx}] Content is not one of `str, list, tuple`. Now {type(content)}: {content}')
    f.write('\n')


def parse_and_save_img(b64_img, img_save_path):
    img = Image.open(io.BytesIO(base64.b64decode(b64_img)))
    img.save(img_save_path)


def write_to_md(md_path, img_folder, parsed_text, md_title):
    with open(md_path, 'w') as f:
        write_md_title(f, md_title, os.path.basename(md_path))
        for idx, t in enumerate(parsed_text):
            if t[1] == 'text':
                write_one_item(f, t[3], t[0])
            elif t[1] == 'img':
                time = datetime.datetime.now()
                img_basename = 'image-' + time.strftime("%Y%m%d_%H%M%S_") + str(datetime.datetime.now().microsecond)
                write_one_item(f, f'![{img_basename}](imgs/{os.path.basename(img_folder)}/{img_basename}.png)', t[0])
                parse_and_save_img(t[3], os.path.join(img_folder, f'{img_basename}.png'))
            elif t[1] == 'code':
                if t[2] is None:
                    code_type = ''
                else:
                    code_type = t[2]
                f.write(f'```{code_type}\n')  # TODO put to func write_one_item
                write_one_item(f, t[3], t[0])
                f.write(f'```\n')
            else:
                raise ValueError(f'[Cell idx {t[0]}] Unexpected parsed ipynb type {t[1]} in {t}')


def confirm_overwrite(md_path, md_filename):
    # TODO also check img folder
    if os.path.exists(md_path):
        print(f'Markdown file {md_filename} has already existed in: {md_path}')
        print('Continue will overwrite existed markdown file')
        confirm_input = input('Continue: [Y/n]')
        if confirm_input == 'Y':
            confirm_input = input('Continue: [Y/n]')
            if confirm_input == 'Y':
                pass
            else:
                exit(0)
        else:
            exit(0)


if __name__ == '__main__':
    args = init_args().parse_args().__dict__

    ipynb_path = args['ipynb_file']
    md_dir = args['md_dir']
    md_filename = args['md_filename']
    if md_filename is None:
        md_filename = os.path.splitext(os.path.basename(ipynb_path))[0]
    if not md_filename.endswith('.md'):
        md_filename = md_filename + '.md'

    md_path = os.path.join(md_dir, md_filename)

    if args['overwrite_confirm'] == 1:
        confirm_overwrite(md_path, md_filename)
    else:
        pass

    if args['img_folder'] is None:
        img_folder = os.path.join(os.path.dirname(md_path), 'imgs', md_filename.rstrip('.md'))
    else:
        img_folder = args['img_folder']
    os.makedirs(img_folder, exist_ok=True)

    ipynb_cells = load_ipynb_cells(ipynb_path, skip_1st_title=args['skip_1st_title'])
    ipynb_text = parse_ipynb_cells(ipynb_cells)
    # print(ipynb_text[:5])
    write_to_md(md_path, img_folder, ipynb_text, args['markdown_title'])
