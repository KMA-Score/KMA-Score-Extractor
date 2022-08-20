import logging

import pandas as pd
import pdfplumber

from tqdm import tqdm


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

    all_subject_score = {}

    logging.info("Extract file {}".format(file))

    pdf_instance = pdfplumber.open(file)

    for i, page in enumerate(tqdm(pdf_instance.pages)):
        table = page.extract_table()

        # Process table
        table_df = pd.DataFrame(table)  # Kinda hack but whatever

        cols_needed = table_df.iloc[1:, [2, 3, 4, 5, 6, 7, 8, 9]]

        # Add to dict

        key = _find_keys(file_dict, i)

        if key not in all_subject_score:
            all_subject_score[key] = []

        all_subject_score[key] += cols_needed.values.tolist()

    return all_subject_score
