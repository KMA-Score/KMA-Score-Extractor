import camelot
import os

# checking ghostscript for Windows environment
if os.name == 'nt':
    import ctypes
    from ctypes.util import find_library

    find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))


def _find_keys(file_dict, page):
    keys = list(file_dict.keys())
    values = list(file_dict.values())

    for i, value in enumerate(values):
        if page in value:
            return keys[i]

    return None


def extract_table(file, file_dict):
    """
    Extract score table from pdf
    :param file: Path to file
    :type file str
    :param file_dict: Dict that contain subjectCode-page mapping
    :type file_dict dict
    :return: A dict that contain subjectCode-Score By StudentCode format
    :rtype: dict
    """
    tables = camelot.read_pdf(file, pages='all')

    all_subject_score = {}

    for i, table in enumerate(tables):
        table_pd = table.df

        if len(table_pd.columns) < 10:
            continue

        # TODO: Fix. OCR sometime merge SDB and StudentName column
        if len(table_pd.columns) == 10:
            cols_needed = table_pd.iloc[1:, [1, 2, 3, 4, 5, 6, 7, 8]]
        else:
            cols_needed = table_pd.iloc[1:, [2, 3, 4, 5, 6, 7, 8, 9]]

        key = _find_keys(file_dict, i)

        if key not in all_subject_score:
            all_subject_score[key] = []

        all_subject_score[key] += cols_needed.values.tolist()

    return all_subject_score
