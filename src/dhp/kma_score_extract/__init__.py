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

    def __init__(self, path, poppler_path, tesseract_path):
        self.poppler_path = poppler_path
        self.tesseract_path = tesseract_path

        if path is None:
            raise Exception("Path must not null")

        self.path = path

    def extract(self):
        # file_path = os.path.join(os.path.abspath(".."), "sample", FILENAME)
        list_img = extract_image(self.path, poppler_path=self.poppler_path)

        # pdf2images = r"E:\PROJECT\KMA\KMA_Score\temp\pdf2images"
        file_dict = subject_spliter(list_img, tesseract_path=self.tesseract_path)

        all_subject = extract_table(self.path, file_dict)

        return all_subject
