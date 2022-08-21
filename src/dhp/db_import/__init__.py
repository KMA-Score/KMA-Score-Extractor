import sqlite3
import logging
import pandas as pd
from dhp.db_import.utils import *
from tqdm import tqdm


class DBImport:
    """
    DB Utilities for create and export database sqlite

    Parameters
    ----------
    db_file: str
        Path to database file

    """

    def __init__(self, db_file):
        self.db = db_file
        self.con = sqlite3.connect(self.db)

        self._create_table_if_not_exist()

    def _create_table_if_not_exist(self):
        logging.info("Checking table if not exist")
        cursor = self.con.cursor()

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
        cursor = self.con.cursor()

        if subject_dict is not None:
            for subjectCode, subjectInfo in tqdm(subject_dict.items()):
                cursor.execute("SELECT id FROM Subjects WHERE Id=?", (subjectCode,))
                rows = cursor.fetchall()

                if len(rows) >= 1:
                    continue

                cursor.execute("INSERT INTO Subjects (Id, NumberOfCredits) VALUES (?,?)",
                               (clean_text(subjectCode), clean_text(subjectInfo['noc'])))

        if data is not None:
            for subjectCode, studentsSubjectData in tqdm(data.items()):
                # studentsSubjectData = data[subjectCode]

                for studentSubjectData in studentsSubjectData:
                    cursor.execute("SELECT id FROM Students WHERE Id=?",
                                   (student_code_format(studentSubjectData[0]),))

                    studentRows = cursor.fetchall()

                    if len(studentRows) < 1:
                        cursor.execute("INSERT INTO Students (Id, Name, Class) VALUES (?,?,?)",
                                       (student_code_format(studentSubjectData[0]),
                                        student_name_clean_text(studentSubjectData[1]),
                                        clean_text(studentSubjectData[2])))

                    cursor.execute("SELECT Id FROM Scores WHERE StudentId=? AND SubjectId=?",
                                   (student_code_format(studentSubjectData[0]), clean_text(subjectCode)))

                    rows = cursor.fetchall()

                    if len(rows) >= 1:
                        cursor.execute('''
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
                        cursor.execute('''
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

            self.con.commit()

            logging.info("Import to DB success")

        else:
            raise Exception("Data cannot be null")

    def export_to_sql(self, file_path):
        """
        Dump database to sql schema
        :param file_path: Path to file location
        :type file_path: str
        :return: No return
        :rtype: void
        """
        if not file_path:
            raise Exception("File path can not be null")

        logging.info("Dump to sql")

        with open(file_path, 'w', encoding='utf-8') as f:
            for line in self.con.iterdump():
                f.write('%s\n' % line)

        logging.info("Successfully export to {}".format(file_path))

    def export_score(self, file_path, file_type='csv'):
        """
        Dump score table in database to multiple format
        :param file_path: Path to file location
        :type file_path str
        :param file_type: Type of output format
        :type file_type str
        :return: No return
        :rtype: void
        """
        if not file_path:
            raise Exception("File path can not be null")

        if file_type not in ['csv', 'excel', 'json']:
            raise Exception("Type must be csv, excel or json")

        logging.info("Dump to {}".format(file_type))

        df = pd.read_sql_query("SELECT * FROM Scores", self.con)

        df.drop(df.columns[0], axis=1, inplace=True)

        if file_type == "csv":
            df.to_csv(file_path)
        elif file_type == "excel":
            df.to_excel(file_path)
        elif file_type == "json":
            df.to_json(file_path)

        logging.info("Successfully export format {} in {}".format(file_type, file_path))
