from pathlib import Path
import sys
import logging
import shutil

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from dhp.kma_score_extract.pdf_to_image import *
from dhp.kma_score_extract.subject_spliter import *
from dhp.kma_score_extract.extract_table import *


def _get_absolute_file_list(path):
    new_file_list = []

    for file in os.listdir(path):
        new_file_list.append(os.path.join(path, file))


class KMAScoreExtract:

    def __init__(self, path, poppler_path=None, temp_path=None):
        self.poppler_path = poppler_path
        self.temp_path = temp_path

        if path is None:
            raise Exception("Path must not null")

        self.path = path

    def extract(self):
        """
        Extract score from pdf
        :return:
        """
        logging.info("Divide page to subject group")

        file_dict = subject_spliter(self.path)

        logging.info(file_dict)

        logging.info("Extract table from pdf")

        all_subject = extract_table(self.path, file_dict)

        return all_subject
