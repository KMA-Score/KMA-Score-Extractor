from dhp_kma.core import KmaScoreCore
from dhp_kma.db.sqlite_handle import Database
import os
from loguru import logger
import sys
from dhp_kma.utils.command_line import *

if __name__ == "__main__":
    args = create_command_line()

    if args.type == "dump":
        PATH = args.path
        log_level = args.debug

        logger.remove()

        if log_level is True:
            logger.add(sys.stderr, level="DEBUG")
        else:
            logger.add(sys.stderr, level="INFO")

        DB_PATH = os.path.join(os.path.abspath("src"), "..", "output/db.db")

        obj = os.scandir(PATH)

        file_list = []

        for entry in obj:
            if entry.is_file():
                file_list.append(entry)

        logger.info("Found {file} files!", file=len(file_list))

        db = Database(db_file_path=DB_PATH)

        for file_name in file_list:
            handler = KmaScoreCore(os.path.join(os.path.abspath('src'), "..", file_name))
            subject_dict, file_score_data = handler.run()

            db.insert_into_db(file_score_data, subject_dict)
