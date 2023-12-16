from loguru import logger
import pandas as pd
import pdfplumber


def _find_keys(file_dict, page):
    keys = list(file_dict.keys())
    values = list(file_dict.values())

    for i, value in enumerate(values):
        if page in value:
            return keys[i]

    return None


def extract_table(process_bar_manager, file_name, file_path, file_dict):
    """
    Extract score table from pdf
    :param process_bar_manager: Instance of enlighten manager
    :type process_bar_manager Any
    :param file_name: file name
    :type file_name str
    :param file_path: Path to file
    :type file_path str
    :param file_dict: Dict that contain subjectCode-page mapping
    :type file_dict dict
    :return: A dict that contain subjectCode-Score By StudentCode format
    :rtype: dict
    """

    all_subject_score = {}

    logger.info("Extract file {}".format(file_name))

    pdf_instance = pdfplumber.open(file_path)

    # create process bar
    task = process_bar_manager.add_task(f"{file_name} - {len(pdf_instance.pages)} pages", total=len(pdf_instance.pages))

    for i, page in enumerate(pdf_instance.pages):
        table = page.extract_table()

        if table is None:
            continue

        # Process table
        table_df = pd.DataFrame(table)

        if len(table_df.columns) < 10:  # Kinda a hack but whatever. LOL and it still WORKS
            continue

        cols_needed = table_df.iloc[1:, [2, 3, 4, 5, 6, 7, 8, 9]]

        # Add to dict

        key = _find_keys(file_dict, i)

        if key not in all_subject_score:
            all_subject_score[key] = []

        all_subject_score[key] += cols_needed.values.tolist()

        process_bar_manager.update(task, advance=1)

    return all_subject_score
