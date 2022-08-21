import json
import os

import fitz
import numpy as np
from tqdm import tqdm

from dhp.kma_score_extract.subject_spliter.ocr import *


def _get_file_list(temp_folder):
    return os.listdir(temp_folder)


def _get_page(file):
    return int(file.split('.')[0])


# TODO: Remove this method
def subject_spliter_ocr(images, gpu):
    """
    DEPRECATED
    :param images: List of PIL image
    :type images list
    :param gpu: Using GPU for OCR process
    :type gpu bool
    :return: Dictionary of SubjectCode-Page Mapping
    :rtype: dict
    """
    file_dict = {}

    global_subject_code = ""

    for i, file in tqdm(enumerate(images)):

        img = np.array(file)

        # hvktmm_img = img[90:145, 150:335] # for pdf dpi 200
        hvktmm_img = img[200:285, 335:665]
        hvktmm = ocr(hvktmm_img, gpu=gpu)

        if hvktmm.upper() == "HỌC VIỆN":
            # subject_code_img = img[315:365, 1360:1650] # for pdf dpi 200
            subject_code_img = img[645:720, 2730:3150]
            subject_code = ocr(subject_code_img, gpu=gpu)

            global_subject_code = subject_code
            file_dict[subject_code] = []
            file_dict[subject_code].append(i)

        else:
            if not global_subject_code:  # check if blank page at start file
                continue

            file_dict[global_subject_code].append(i)

    return file_dict


def subject_spliter(pdf_file):
    """
    Divide page by subject
    :param pdf_file: Path to PDF file
    :type pdf_file str
    :return: Dictionary of SubjectCode-Page Mapping
     :rtype: dict
    """
    file_dict = {}
    subject_dict = {}

    global_subject_code = ""

    with fitz.open(pdf_file) as pages:
        subject_mapping_file = open(
            os.path.join(os.path.abspath('dhp'), 'kma_score_extract', 'subject_spliter', 'subjectNameMapping.json'),
            encoding="utf-8")
        subject_mapping = json.loads(subject_mapping_file.read())

        for i, page in enumerate(tqdm(pages)):
            page_content = page.get_text()

            if not page_content:
                continue

            page_content_line = page_content.split("\n")

            student_code_line = ""
            subject_noc = ""

            for pcl_index, x in enumerate(page_content_line):
                if x.__contains__('Mã học phần'):
                    student_code_line = x

                if x.__contains__('Số TC:'):
                    subject_noc = page_content_line[pcl_index + 1]

            if not student_code_line:
                if not global_subject_code:  # Prevent cover and not score page
                    continue

                subject_code = global_subject_code  # Prevent page don't have subject code
            else:
                subject_code = student_code_line.split(":")[1].strip()
                global_subject_code = subject_code

            if subject_code not in subject_dict.keys():
                subject_data = next((item for item in subject_mapping if item["subjectCode"] == subject_code), None)

                if subject_data is not None:
                    subject_name = subject_data.get('name', 'NULL')
                else:
                    subject_name = "NULL"

                subject_dict[subject_code] = {
                    'noc': subject_noc,
                    'name': subject_name
                }

            if subject_code not in file_dict.keys():
                file_dict[subject_code] = [i]
            else:
                file_dict[subject_code].append(i)

    return file_dict, subject_dict
