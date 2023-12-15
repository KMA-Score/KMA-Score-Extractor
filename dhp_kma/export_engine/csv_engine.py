from loguru import logger
import csv
from tqdm import tqdm
from os import path

from dhp_kma.utils.string import *
from dhp_kma.utils.time_utils import get_timestamp


class CsvEngine:
    def __init__(self, folder_path, output_mode="tsv"):
        timestamp = get_timestamp()

        self.__delimiter = '\t' if output_mode == "tsv" else ','
        self.__output_path = path.join(folder_path, str(timestamp))

        self.__score_path = os.path.join(self.__output_path, "score.{}".format(output_mode))
        self.__subject_path = os.path.join(self.__output_path, "subject.{}".format(output_mode))
        self.__student_path = os.path.join(self.__output_path, "student.{}".format(output_mode))

        # tf who need this when output is unique
        # self.__reset_csv()
        self.__check_missing_output_dir(self.__output_path)

        # Score engine
        logger.info("Init Score CSV Engine ...")
        score_header_field = ['StudentId', 'SubjectId', 'FirstComponentScore', 'SecondComponentScore', 'ExamScore',
                              'AvgScore', 'AlphabetScore']
        self.__score_file = open(self.__score_path, mode="w", encoding="utf-8", newline="")
        self.__score_writer = csv.DictWriter(self.__score_file, fieldnames=score_header_field,
                                             delimiter=self.__delimiter)

        # Subject engine
        logger.info("Init Subject CSV Engine ...")
        subject_header_field = ["Id", "Name", "NumberOfCredits"]
        self.__subject_file = open(self.__subject_path, mode="w", encoding="utf-8", newline="")
        self.__subject_writer = csv.DictWriter(self.__subject_file, fieldnames=subject_header_field,
                                               delimiter=self.__delimiter)

        # Student engine
        logger.info("Init Student CSV Engine ...")
        student_header_field = ["Id", "Name", "Class"]
        self.__student_file = open(self.__student_path, mode="w", encoding="utf-8", newline="")
        self.__student_writer = csv.DictWriter(self.__student_file, fieldnames=student_header_field,
                                               delimiter=self.__delimiter)

        self.__create_default_header()

    def __check_missing_output_dir(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def __reset_csv(self):
        logger.info("Reset CSV...")

        if os.path.exists(self.__score_path):
            os.remove(self.__score_path)
        else:
            logger.info("No Score CSV found! Skip reset")

        if os.path.exists(self.__subject_path):
            os.remove(self.__subject_path)
        else:
            logger.info("No Subject CSV found! Skip reset")

        if os.path.exists(self.__student_path):
            os.remove(self.__student_path)
        else:
            logger.info("No Student CSV found! Skip reset")

    def __create_default_header(self):
        self.__score_writer.writeheader()
        self.__subject_writer.writeheader()
        self.__student_writer.writeheader()

    def run_score(self, data):
        insert_rows = []

        logger.info("Export to score to CSV")

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

        self.__score_writer.writerows(insert_rows)

    def run_subject(self, data):
        insert_rows = []

        logger.info("Export to subject to CSV")

        for subjectCode, subjectData in tqdm(data.items()):
            insert_dict = {
                "Id": clean_text(subjectCode),
                "Name": clean_text(subjectData['name']),
                "NumberOfCredits": clean_text(subjectData['noc'])
            }

            insert_rows.append(insert_dict)

        self.__subject_writer.writerows(insert_rows)

    def run_student(self, data):
        insert_rows = []

        logger.info("Export to student to CSV")

        for studentsSubjectData in tqdm(data.values()):
            for studentSubjectData in studentsSubjectData:
                insert_dict = {
                    "Id": student_code_format(studentSubjectData[0]),
                    "Name": clean_text(studentSubjectData[1]),
                    "Class": clean_text(studentSubjectData[2]),
                }

                insert_rows.append(insert_dict)

        self.__student_writer.writerows(insert_rows)

    def close_file(self):
        self.__score_file.close()
        self.__subject_file.close()
        self.__student_file.close()
