import sys
from loguru import logger
import os

from dhp_kma.core import KmaScoreCore
from dhp_kma.export_engine.csv_engine import CsvEngine
from dhp_kma.export_engine.json_engine import csv_to_json
from dhp_kma.export_engine.sql_engine import generate_sql
from dhp_kma.utils.command_line import create_command_line
from dhp_kma.utils.sanity_check import sanity_check


def dump_opt():
    PATH = args.path
    log_level = args.debug

    logger.remove()

    if log_level is True:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")

    sanity_check()

    if args.output_path:
        OUTPUT_FOLDER_PATH = args.output_path
    else:
        OUTPUT_FOLDER_PATH = os.path.join(os.path.abspath("."), "output")

    obj = os.scandir(PATH)

    file_list = []

    for entry in obj:
        if entry.is_file():
            file_list.append(entry)

    logger.info("Found {file} files!", file=len(file_list))

    export_engine = CsvEngine(folder_path=OUTPUT_FOLDER_PATH)

    for file_name in file_list:
        handler = KmaScoreCore(os.path.join(os.path.abspath("."), "sample", file_name))
        subject_dict, file_score_data = handler.run()

        export_engine.run_score(file_score_data)
        export_engine.run_subject(subject_dict)
        export_engine.run_student(file_score_data)

    export_engine.close_file()


if __name__ == "__main__":
    args, parser = create_command_line()

    if args.type is None:
        parser.print_help()

    if args.type == "dump":
        dump_opt()
    elif args.type == "tool":
        if args.tool_type == "c2j" or args.tool_type == "csv2json":
            csv_to_json(args.input_path, args.output_path)
        elif args.tool_type == "sqlGenerate" or args.tool_type == "sqlgen":
            generate_sql(args.input_path, args.output_path)
