import sys
from loguru import logger
import os
import pickle
import multiprocessing
from time import time
from loky import get_reusable_executor, wait
import gc
from shutil import rmtree

from dhp_kma.core import KmaScoreCore
from dhp_kma.export_engine.csv_engine import CsvEngine
from dhp_kma.export_engine.json_engine import csv_to_json
from dhp_kma.export_engine.sql_engine import *
from dhp_kma.utils.command_line import create_command_line
from dhp_kma.utils.sanity_check import sanity_check
from dhp_kma.utils.string import chunk_list

# Register temp folder
temp_dir = os.path.join(os.path.abspath("."), "temp")

if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)


def process_work(chunked_file_list):
    for file in chunked_file_list:
        file_name, file_index = file

        handler = KmaScoreCore(file_name)
        subject_dict, file_score_data = handler.run()

        temp_file = open(os.path.join(temp_dir, "{}.bin".format(file_index)), "wb")
        pickle.dump((subject_dict, file_score_data), temp_file)
        temp_file.close()

        # Clear memory
        del subject_dict
        del file_score_data
        gc.collect()


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
    inter_file_list = list(map(lambda x: (os.path.join(input_path, x[1]), x[0]), enumerate(file_list)))

    logger.info("Found {file} files!", file=len(inter_file_list))

    # chunk list file
    chunked_list = list(chunk_list(inter_file_list, 3))

    # init process pool
    executor = get_reusable_executor(max_workers=multiprocessing.cpu_count(), reuse=True)
    futures = {executor.submit(process_work, chunk): chunk for chunk in chunked_list}

    # wait for all process done
    wait(futures, return_when="ALL_COMPLETED")

    # init export engine
    export_engine = CsvEngine(folder_path=output_folder_path, output_mode="tsv")

    # scan temp dir and export to tsv
    temp_obj = os.scandir(temp_dir)
    temp_file_list = filter(lambda x: x.is_file() and x.name.endswith(".bin"), temp_obj)

    for temp_file in temp_file_list:
        temp_file_path = os.path.join(temp_dir, temp_file.name)
        temp_file = open(temp_file_path, 'rb')
        (subject_dict, file_score_data) = pickle.load(temp_file)

        export_engine.run_score(file_score_data)
        export_engine.run_subject(subject_dict)
        export_engine.run_student(file_score_data)

        temp_file.close()

    rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    start_time = time()

    args, parser = create_command_line()

    if args.type is None:
        parser.print_help()

    if args.type == "dump":
        dump_opt()
    elif args.type == "tool":
        if args.tool_type == "c2j" or args.tool_type == "csv2json":
            csv_to_json(args.input_path, args.output_path)
        elif args.tool_type == "sqlGenerateScore" or args.tool_type == "sqlgensco":
            generate_sql_score(args.input_path, args.output_path)
        elif args.tool_type == "sqlGenerateStudent" or args.tool_type == "sqlgenstu":
            generate_sql_student(args.input_path, args.output_path)
        elif args.tool_type == "sqlGenerateSubject" or args.tool_type == "sqlgensub":
            generate_sql_subject(args.input_path, args.output_path)

    print("Total time: {}s".format(round(time() - start_time, 2)))
