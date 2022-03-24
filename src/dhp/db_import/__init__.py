import sqlite3


class DBImport:
    def __init__(self, db_file):
        self.db = db_file
        self.con = None

    def insert_into_db(self, data):
        self.con = sqlite3.connect(self.db)
        cursor = self.con.cursor()
