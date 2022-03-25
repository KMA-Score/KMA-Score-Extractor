import os
from dhp.kma_score_extract.subject_spliter.ocr import *
from tqdm import tqdm
import numpy as np


def _get_file_list(temp_folder):
    return os.listdir(temp_folder)


def _get_page(file):
    return int(file.split('.')[0])


def subject_spliter(images):
    """
    Divide page by subject
    :param images: List of PIL image
    :type images list
    :return: Dictionary of SubjectCode-Page Mapping
    :rtype: dict
    """
    file_dict = {}

    global_subject_code = ""

    for i, file in tqdm(enumerate(images)):

        img = np.array(file)

        # hvktmm_img = img[90:145, 150:335] # for pdf dpi 200
        hvktmm_img = img[200:285, 335:665]
        hvktmm = ocr(hvktmm_img)

        if hvktmm.upper() == "HỌC VIỆN":
            # subject_code_img = img[315:365, 1360:1650] # for pdf dpi 200
            subject_code_img = img[645:720, 2730:3150]
            subject_code = ocr(subject_code_img)

            global_subject_code = subject_code
            file_dict[subject_code] = []
            file_dict[subject_code].append(i)

        else:
            if not global_subject_code:  # check if blank page at start file
                continue

            file_dict[global_subject_code].append(i)

    return file_dict
