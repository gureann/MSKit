import os

from PyPDF2 import PdfFileMerger


def merge_pdfs(dir_path, out_file):
    pdf_lst = [f for f in os.listdir(dir_path) if f.lower().endswith('.pdf')]
    pdf_lst = [os.path.join(dir_path, f) for f in pdf_lst]

    file_merger = PdfFileMerger()
    for pdf in pdf_lst:
        file_merger.append(pdf, import_bookmarks=False)

    file_merger.write(out_file)
