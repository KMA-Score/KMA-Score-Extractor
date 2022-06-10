from dhp.db_import import *
import os
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    db = DBImport(db_file=os.path.join(os.path.abspath(".."), "output", "database.db"))

    # Export to sql
    db.export_to_sql(file_path=os.path.join(os.path.abspath(".."), "output", "KKA_Score.sql"))

    # Export to csv
    # db.export_score(file_path=os.path.join(os.path.abspath(".."), "output", "KKA_Score.csv"), file_type="csv")

    # Export to excel
    # db.export_score(file_path=os.path.join(os.path.abspath(".."), "output", "KKA_Score.xlsx"), file_type="excel")

    # Export to json
    db.export_score(file_path=os.path.join(os.path.abspath(".."), "output", "KKA_Score.json"), file_type="json")
