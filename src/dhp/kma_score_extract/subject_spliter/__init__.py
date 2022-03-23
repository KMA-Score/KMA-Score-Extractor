import os
import cv2
from src.dhp.kma_score_extract.subject_spliter.tessaract import *


# yy xx
# crop_img = img[90:145, 150:335] #HVKTMM
# img = img[315:365, 230:900] #Subject Name
# img = img[315:365, 1360:1650] # subject code


def _get_file_list(temp_folder):
    return os.listdir(temp_folder)


def _get_page(file):
    return int(file.split('.')[0])


def subject_spliter(temp_folder, tesseract_path):
    file_list = _get_file_list(temp_folder)

    file_dict = {}

    temp_subject_code = ''

    for file in file_list:
        file_path = os.path.join(temp_folder, file)

        img = cv2.imread(file_path, 0)

        hvktmm_img = img[90:145, 150:335]
        hvktmm = ocr(hvktmm_img, tesseract_path)

        if hvktmm.upper() == "HỌC VIỆN":
            subject_code_img = img[315:365, 1360:1650]
            subject_code = ocr(subject_code_img, tesseract_path)
            file_dict[subject_code] = [_get_page(file)]
            temp_subject_code = subject_code
        else:
            file_dict[temp_subject_code].append(_get_page(file))

    return file_dict
