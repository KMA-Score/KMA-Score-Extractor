import sqlite3
from dhp.db_import.utils import *


class DBImport:
    def __init__(self, db_file):
        self.db = db_file
        self.con = sqlite3.connect(self.db)

        self._create_table_if_not_exist()

    def _create_table_if_not_exist(self):
        cursor = self.con.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS studentScore (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentCode VARCHAR(30),
            subjectCode VARCHAR(30),
            TP1 VARCHAR(5),
            TP2 VARCHAR(5),
            THI VARCHAR(5),
            TONGKET VARCHAR(5),
            DIEMCHU VARCHAR(5)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS studentInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentCode VARCHAR(30),
            name VARCHAR(255),
            class VARCHAR(20)
        );
        """)

    def insert_into_db(self, data):
        if data is not None:
            cursor = self.con.cursor()

            for subjectCode in data:
                studentsSubjectData = data[subjectCode]

                for studentSubjectData in studentsSubjectData:
                    cursor.execute("SELECT id FROM studentScore WHERE studentCode=? AND subjectCode=?",
                                   (student_code_format(studentSubjectData[0]), clean_text(subjectCode)))

                    rows = cursor.fetchall()

                    if len(rows) >= 1:
                        cursor.execute('''
                        UPDATE studentScore 
                        SET 
                            TP1=?,
                            TP2=?,
                            THI=?,
                            TONGKET=?,
                            DIEMCHU=?
                        WHERE
                             studentCode=? AND subjectCode=?
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
                        INSERT INTO studentScore (
                            studentCode,
                            subjectCode, 
                            TP1,
                            TP2,
                            THI,
                            TONGKET,
                            DIEMCHU) 
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

        else:
            raise Exception("Data cannot be null")
