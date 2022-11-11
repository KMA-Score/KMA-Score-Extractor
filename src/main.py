from dhp_kma.core import KmaScoreCore
from dhp_kma.db.sqlite_handle import Database
import os
from loguru import logger
import sys

if __name__ == "__main__":
    PATH = "../sample"
    DB_PATH = "../output/db.db"

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    obj = os.scandir(PATH)

    file_list = []

    for entry in obj:
        if entry.is_file():
            file_list.append(entry)

    logger.info("Found {file} files!", file=len(file_list))

    db = Database(db_file_path=DB_PATH)

    for file_name in file_list:
        handler = KmaScoreCore(os.path.join(PATH, file_name))
        subject_dict, file_score_data = handler.run()

        db.insert_into_db(file_score_data, subject_dict)
