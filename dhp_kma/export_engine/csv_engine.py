from loguru import logger
import csv
import os
from tqdm import tqdm

from dhp_kma.utils.string import *


class CsvEngine:
    def __init__(self, file_path):
        self._path = file_path

        self.__reset_csv()

        logger.info("Init CSV Engine ...")

        header_field_name = ['StudentId', 'SubjectId', 'FirstComponentScore', 'SecondComponentScore', 'ExamScore',
                             'AvgScore', 'AlphabetScore']

        self.__file = open(file_path, mode="w", encoding="utf-8", newline="")

        self.__writer = csv.DictWriter(self.__file, fieldnames=header_field_name)

        self.__create_default_header()

    def __reset_csv(self):
        logger.info("Reset CSV...")

        if os.path.exists(self._path):
            os.remove(self._path)
        else:
            logger.info("No CSV found! Skip reset")

    def __create_default_header(self):
        self.__writer.writeheader()

    def run_score(self, data):
        insert_rows = []

        for subjectCode, studentsSubjectData in tqdm(data.items()):
            for studentSubjectData in studentsSubjectData:
                insert_dict = {
                    "StudentId": student_code_format(studentSubjectData[0]),
                    "SubjectId": clean_text(subjectCode),
                    "FirstComponentScore": clean_text(studentSubjectData[3]),
                    "SecondComponentScore": clean_text(studentSubjectData[4]),
                    "ExamScore": clean_text(studentSubjectData[5]),
                    "AvgScore": clean_text(studentSubjectData[6]),
                    "AlphabetScore": clean_text(studentSubjectData[7])
                }

                insert_rows.append(insert_dict)

        self.__writer.writerows(insert_rows)

    def close_file(self):
        self.__file.close()
