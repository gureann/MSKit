import os
import re
import sys
import typing

import numpy as np
import pandas as pd

from .text_kit import find_substring


def dask_series_map(
        ddf_series,
        map_dict: dict,
        map_size_threshold=None,
        client=None
):
    if map_size_threshold is None:
        map_size_threshold = 1e5
    if sys.getsizeof(map_dict) > map_size_threshold:
        if client is None:
            raise ValueError(
                f'The size of input map is larger than threshold {map_size_threshold}, '
                f'a client is needed to pass in this function to pre-submit large data')

        def make_mapping():
            return map_dict

        mapping = client.submit(make_mapping)
        return client.submit(ddf_series.map, mapping).result()
    else:
        return ddf_series.map(map_dict)


def split_row_with_sep_cell(
        df,
        split_cols=(),
        new_cols=(),
        drop=(),
        seps=(),
) -> pd.DataFrame:
    """
    drop columns if new col names are assigned, or manurally control. But columns with no new col names are always dropped
    """
    df[split_cols] = df[split_cols].astype(str)
    df = (
        df
            .drop(['AllProteins', 'Positions within protein', 'Best Ascores', 'IsFirstProtein'], axis=1)
            .join(pd.concat([
            (df[col].str.split(sep, expand=True).stack()
             .reset_index(level=0).set_index('level_0')
             .rename(columns={0: renamed_col}))
            for col, renamed_col, sep in [
                ('AllProteins', 'SingleProtein', ';'),
                ('Positions within protein', 'ProteinPhosPos', '/'),
                ('Best Ascores', 'Best Ascore', ','),
                ('IsFirstProtein', 'IsFirstProtein', ';')]
        ], axis=1))).reset_index(drop=True)
    return df


def select_row_with_target_col(df, ident, colname, return_col_list=None):
    _df = df[df[colname].str.contains(ident)]
    if return_col_list:
        return _df[return_col_list]
    else:
        return _df


def df_to_file(df: pd.DataFrame, path: str, *args, **kws) -> None:
    if path.endswith('.xlsx') or path.endswith('.xls'):
        df.to_excel(path, *args, **kws)
    elif path.endswith('.csv'):
        df.to(path, sep=',', *args, **kws)
    elif path.endswith('.txt') or path.endswith('.tsv'):
        df.to(path, sep='\t', *args, **kws)
    else:
        raise ValueError


def load_file_to_df(
        path: str,
        load_all_sheets: bool = True,
        custom_raise_for_other_formats: Exception = None,
        *args,
        **kws
) -> typing.Union[pd.DataFrame, typing.Dict[str, pd.DataFrame]]:
    if path.endswith('.xlsx') or path.endswith('.xls'):
        if load_all_sheets:
            with pd.ExcelFile(path) as e:
                sheets = e.sheet_names
                if len(sheets) == 1:
                    df = e.parse(sheets[0], *args, **kws)
                else:
                    df = e.parse(sheets, *args, **kws)
        else:
            df = pd.read_excel(path, *args, **kws)
    elif path.endswith('.csv'):
        df = pd.read_csv(path, sep=',', *args, **kws)
    elif path.endswith('.txt') or path.endswith('.tsv'):
        df = pd.read_csv(path, sep='\t', *args, **kws)
    else:
        if custom_raise_for_other_formats is not None:
            raise custom_raise_for_other_formats
        else:
            raise ValueError(f'Only the following formats are included: `.xlsx, .xls, .txt, .tsv, .csv`. '
                             f'Current file: {os.path.basename(path)}')
    return df


def extract_df_with_col_ident(original_df, identifiers, focus_col, return_col_list=None):
    if isinstance(identifiers, str):
        target_df = select_row_with_target_col(original_df, identifiers, focus_col, return_col_list)
        return target_df
    elif isinstance(identifiers, list):
        target_df_list = [select_row_with_target_col(original_df, _, focus_col, return_col_list) for _ in identifiers]
        return target_df_list
    else:
        return None


def df_keep_block_first_line(df_with_blocks, filtered_col_name):
    """
    To get the first line when the file is consist of many blocks which means some same values are in the same column in neighboring lines
    This may keep same values in the selected columns because the blocks have same values in the selected column may not be neighboring
    :param df_with_blocks:
    :param filtered_col_name:
    :return:
    """
    non_block_df = df_with_blocks[df_with_blocks[filtered_col_name] != df_with_blocks[filtered_col_name].shift(1)]
    return non_block_df


def match_protein_groups(x, protein_list, col='PG.ProteinGroups', delimiter=';'):
    if isinstance(x[col], float):
        return False
    if set(x[col].split(delimiter)) & set(protein_list):
        return True
    return False


def split_protein_groups(x, col=None):
    if not isinstance(x, str):
        acc = x[col]
    else:
        acc = x
    if pd.isna(acc):
        return np.nan
    acc = acc.split(';')[0].strip()
    return acc


def df_split_protein_groups(df, col='PG.ProteinAccessions'):
    first_protein = df.apply(split_protein_groups, col=col, axis=1)
    df['FirstProtein'] = first_protein
    return df


def add_protein_type(x, protein_content, col='FirstProtein'):
    acc = split_protein_groups(x, col=col)
    if pd.isna(acc):
        return np.nan
    for protein_type, acc_list in protein_content.items():
        if acc in acc_list:
            return protein_type
    return 'Others'


def df_add_protein_type(df, col, protein_content, used_type=None, return_col='ProteinType'):
    if isinstance(protein_content, list):
        protein_content = {used_type: protein_content}
    type_series = df.apply(add_protein_type, protein_content=protein_content, col=col, axis=1)
    df[return_col] = type_series
    return df


def filter_prob(
        x,
        find_col,
        prob_col,
        mod_name='(Phospho (STY))',
        recept_prob=0.75,
        refute_prob=0.75):
    find_col_content = x[find_col]
    if mod_name not in find_col_content:
        return True

    prob_col_content = x[prob_col]
    if pd.isna(prob_col_content):
        return True

    if f'(' not in prob_col_content:
        return True

    strippep, modpos, mods = find_substring(find_col_content.replace('_', ''), '(', ')')
    strippep, prob_pos, probs = find_substring(prob_col_content.replace('_', ''), '(', ')')

    for pos in prob_pos:
        prob_idx = prob_pos.index(pos)

        prob = float(probs[prob_idx].strip('()'))
        if pos in modpos:
            if prob <= recept_prob:
                return False
        else:
            if prob > refute_prob:
                return False
    return True


def __filter_prob(
        x,
        find_col,
        prob_col,
        ident='ph',
        recept_prob=0.75,
        refute_prob=0.75):
    """
    :param x: one row of the target dataframe
    :param find_col: colname of col contains sequence with determined label. Example: col 'Modified sequence' _(ac)AAAAAAAAAAAAGDS(ph)DS(ph)WDADTFSM(ox)EDPVRK_
    :param prob_col: colname of col contains sequence with probability. Example: col 'Phospho (STY) Probabilities' AAAAAAAAAAAAGDS(0.876)DS(0.887)WDADT(0.161)FS(0.077)MEDPVRK
    """
    # TODO 这里改成所有含 Probability 的列都 filter，单列filter可选

    find_col_content = x[find_col]
    # To avoid error if there is no mod in the seq. 'Modified sequence' will
    # have no Parentheses
    if f'({ident})' not in find_col_content:
        return True
    prob_col_content = x[prob_col]
    # To avoid error if there is no target var mod in the seq. Prob col will
    # be NaN

    if pd.isna(prob_col_content):
        return True

    if f'(' not in prob_col_content:
        return True

    # replace_pattern = re.compile(rf'\([^{ident}]+\)')  # TODO 这里好像是对 p h 两个字母单独 find
    replace_pattern = re.compile(rf'\((?!{ident}).+?\)')
    ident_find_seq = re.sub(
        replace_pattern,
        '',
        find_col_content).replace(
        '_',
        '')
    split_find_col = re.split(r'[\(\)]', ident_find_seq)[::2]
    split_prob_col = re.split(r'[\(\)]', prob_col_content)
    find_seq_sum = [''.join(split_find_col[:i + 1])
                    for i in range(len(split_find_col))]
    prob_seq_sum = ''
    # 这里因为 prob col 中的位点概率会给出所有可能分配位点的概率值
    # 但是 sequence 里没有过 cutoff 的则没有给出修饰信息，即 (ph)
    # 因此通过 prob col 得到的 sequence 可能不在分割出的 mod sequence 列中
    # 这里设置 refute prob 是指没有给出修饰位点但是这个位点的 prob 超过了一定的值
    for i in range(0, len(split_prob_col) - 1, 2):
        prob_seq_sum += split_prob_col[i]
        if prob_seq_sum in find_seq_sum:
            if float(split_prob_col[i + 1]) <= recept_prob:
                return False
        else:
            if float(split_prob_col[i + 1]) > refute_prob:
                return False
    return True
