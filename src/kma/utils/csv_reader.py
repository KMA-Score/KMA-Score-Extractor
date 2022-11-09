import csv
import os
from loguru import logger


def load_csv(path: str):
    list_return = []

    with open(path, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            list_return.append(row)

    return list_return


def load_subject_mapping():
    mapping_path = os.path.join(os.path.join('data'), 'subjectNameMapping.csv')

    logger.info("Loading subject mapping into memory")

    return load_csv(mapping_path)
