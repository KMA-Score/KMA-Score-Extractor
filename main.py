import os
import sys
from time import time

from dhp_kma.dumper import pdf_dumper
from dhp_kma.export_engine.json_engine import csv_to_json
from dhp_kma.export_engine.sql_engine import *
from dhp_kma.utils.command_line import create_command_line
from dhp_kma.utils.sanity_check import sanity_check


def dump_opt():
    input_path = os.path.abspath(args.path)
    log_level = args.debug

    # Clear log
    logger.remove()

    if log_level is True:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")

    sanity_check()

    if args.output_path:
        output_folder_path = args.output_path
    else:
        output_folder_path = os.path.join(os.path.abspath("."), "output")

    # scan input folder
    obj = os.scandir(input_path)

    # filter only pdf file and convert to tuple (file path, index)
    file_list = filter(lambda x: x.is_file() and x.name.endswith(".pdf"), obj)
    inter_file_list = list(map(lambda x: (x[1].name, os.path.join(input_path, x[1]), x[0]), enumerate(file_list)))

    logger.info("Found {file} files!", file=len(inter_file_list))

    # pdf dump
    pdf_dumper(inter_file_list, output_folder_path)


if __name__ == "__main__":
    start_time = time()

    args, parser = create_command_line()

    if args.type is None:
        parser.print_help()

    if args.type == "dump":
        dump_opt()
    elif args.type == "tools":
        if args.tool_type == "c2j" or args.tool_type == "csv2json":
            csv_to_json(args.input_path, args.output_path)
        elif args.tool_type == "sqlGenerate" or args.tool_type == "sqlgen":
            sql_gen(args.input_path, args.output_path)

    print(f"\nTotal time: {time() - start_time:.3f}s")
