from pathlib import Path
import sys

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

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        """
        Extract score from pdf
        :return:
        """

        logging.info("Divide page to subject group")

        file_dict, subject_dict = subject_spliter(self.file_path)

        logging.info("File Dict: {}".format(file_dict))

        logging.info("Number Of Credit Dict: {}".format(subject_dict))

        logging.info("Extract table from pdf")

        all_subject = extract_table(self.file_path, file_dict)

        return all_subject, subject_dict
