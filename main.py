from dhp_kma.core import KmaScoreCore
from dhp_kma.db.sqlite_handle import Database
import os
import sys
from dhp_kma.utils.command_line import *
from dhp_kma.utils.sanity_check import *

if __name__ == "__main__":
    args, parser = create_command_line()

    if args.type is None:
        parser.print_help()
        exit(0)

    if args.type == "dump":
        PATH = args.path
        log_level = args.debug

        logger.remove()

        if log_level is True:
            logger.add(sys.stderr, level="DEBUG")
        else:
            logger.add(sys.stderr, level="INFO")

        sanity_check()

        if args.db_path:
            DB_PATH = args.db_path
        else:
            DB_PATH = os.path.join(os.path.abspath("."), "output/db.db")

        obj = os.scandir(PATH)

        file_list = []

        for entry in obj:
            if entry.is_file():
                file_list.append(entry)

        logger.info("Found {file} files!", file=len(file_list))

        db = Database(db_file_path=DB_PATH)

        for file_name in file_list:
            handler = KmaScoreCore(os.path.join(os.path.abspath("."), "sample", file_name))
            subject_dict, file_score_data = handler.run()

            db.insert_into_db(file_score_data, subject_dict)
