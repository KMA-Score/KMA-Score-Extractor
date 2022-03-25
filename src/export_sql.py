from dhp.db_import import *
import os
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    db = DBImport(db_file=os.path.join(os.path.abspath(".."), "output", "database.db"))

    db.export_to_sql(file_path=os.path.join(os.path.abspath(".."), "output", "KKA_Score.sql"))
