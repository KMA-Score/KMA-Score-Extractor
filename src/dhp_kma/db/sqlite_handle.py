from loguru import logger
import sqlite3
from dhp_kma.utils.string import *
from tqdm import tqdm
import os


class Database:
    def __init__(self, db_file_path):
        self.__db_path = db_file_path

        self.__reset_database()

        logger.info("Init database connection ...")

        self.__con = sqlite3.connect(self.__db_path)

        self.__create_table_if_not_exist()

    def __reset_database(self):
        logger.info("Reset sqlite database")
        os.remove(self.__db_path)

    def __create_table_if_not_exist(self):
        logger.info("Creating table if not exist")
        cursor = self.__con.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Scores (
            `Id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `StudentId` VARCHAR(8) DEFAULT NULL,
            `SubjectId` VARCHAR(10) DEFAULT NULL,
            `FirstComponentScore` VARCHAR(5) DEFAULT NULL,
            `SecondComponentScore` VARCHAR(5) DEFAULT NULL,
            `ExamScore` VARCHAR(5) DEFAULT NULL,
            `AvgScore` VARCHAR(5) DEFAULT NULL,
            `AlphabetScore` VARCHAR(5) DEFAULT NULL
        )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Students` (
                `Id` VARCHAR(12) PRIMARY KEY NOT NULL,
                `Name` VARCHAR(40) DEFAULT NULL,
                `Class` VARCHAR(7) DEFAULT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Subjects` (
                `Id` VARCHAR(10) PRIMARY KEY NOT NULL,
                `Name` VARCHAR(100) DEFAULT NULL,
                `NumberOfCredits` VARCHAR(2) DEFAULT NULL
            )
        """)

    def insert_into_db(self, data, subject_dict):
        """
        Insert into database from Dict
        :param data: Dict from KMA_Score_Extract
        :type data: dict
        :param subject_dict: Dict of subject info
        :type subject_dict: dict
        :return: This function no return
        :rtype: void
        """
        cursor = self.__con.cursor()

        if subject_dict is not None:
            logger.info("Import subject name to database")

            for subjectCode, subjectInfo in tqdm(subject_dict.items()):
                cursor.execute("SELECT id FROM Subjects WHERE Id=?", (subjectCode,))
                rows = cursor.fetchall()

                if len(rows) >= 1:
                    continue

                cursor.execute("INSERT INTO Subjects (Id,Name, NumberOfCredits) VALUES (?,?,?)",
                               (clean_text(subjectCode), clean_text(subjectInfo['name']),
                                clean_text(subjectInfo['noc'])))

        if data is not None:
            logger.info("Import student score to database")

            for subjectCode, studentsSubjectData in tqdm(data.items()):
                # studentsSubjectData = data[subjectCode]

                for studentSubjectData in studentsSubjectData:
                    self_cursor = self.__con.cursor()

                    self_cursor.execute("SELECT id FROM Students WHERE Id=?",
                                        (student_code_format(studentSubjectData[0]),))

                    studentRows = self_cursor.fetchall()

                    if len(studentRows) < 1:
                        self_cursor.execute("INSERT INTO Students (Id, Name, Class) VALUES (?,?,?)",
                                            (student_code_format(studentSubjectData[0]),
                                             student_name_clean_text(studentSubjectData[1]),
                                             clean_text(studentSubjectData[2])))

                    self_cursor.execute("SELECT Id FROM Scores WHERE StudentId=? AND SubjectId=?",
                                        (student_code_format(studentSubjectData[0]), clean_text(subjectCode)))

                    rows = self_cursor.fetchall()

                    if len(rows) >= 1:
                        self_cursor.execute('''
                        UPDATE Scores 
                        SET 
                            FirstComponentScore=?,
                            SecondComponentScore=?,
                            ExamScore=?,
                            AvgScore=?,
                            AlphabetScore=?
                        WHERE
                             StudentId=? AND SubjectId=?
                        ''', (
                            clean_text(studentSubjectData[3]),
                            clean_text(studentSubjectData[4]),
                            clean_text(studentSubjectData[5]),
                            clean_text(studentSubjectData[6]),
                            clean_text(studentSubjectData[7]),
                            student_code_format(studentSubjectData[0]),
                            clean_text(subjectCode)
                        ))

                    else:
                        self_cursor.execute('''
                        INSERT INTO Scores (
                            StudentId,
                            SubjectId,
                            FirstComponentScore,
                            SecondComponentScore,
                            ExamScore,
                            AvgScore,
                            AlphabetScore) 
                        VALUES (?,?,?,?,?,?,?);''', (
                            student_code_format(studentSubjectData[0]),
                            clean_text(subjectCode),
                            clean_text(studentSubjectData[3]),
                            clean_text(studentSubjectData[4]),
                            clean_text(studentSubjectData[5]),
                            clean_text(studentSubjectData[6]),
                            clean_text(studentSubjectData[7]))
                                            )

                    # Todo: Need to find out in or out loop better
                    self.__con.commit()
                    self_cursor.close()

            logger.info("Import to DB success")

        else:
            raise Exception("Data cannot be null")
