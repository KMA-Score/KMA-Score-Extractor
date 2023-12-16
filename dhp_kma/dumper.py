import gc
import pickle
import multiprocessing
import os
import traceback
from shutil import rmtree
import enlighten

from loguru import logger
from loky import get_reusable_executor
from dhp_kma.utils.string import chunk_list
from dhp_kma.core import KmaScoreCore
from dhp_kma.export_engine.csv_engine import CsvEngine

# Register temp folder
temp_dir = os.path.join(os.path.abspath("."), "temp")

if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

process_bar_manager = enlighten.get_manager()


def _process_work(chunked_file_list):
    for file in chunked_file_list:
        file_name, file_path, file_index = file

        handler = KmaScoreCore(file_name, file_path)
        subject_dict, file_score_data = handler.run()

        temp_file = open(os.path.join(temp_dir, "{}.bin".format(file_index)), "wb")
        pickle.dump((subject_dict, file_score_data), temp_file)
        temp_file.close()

        # Clear memory
        del subject_dict
        del file_score_data
        gc.collect()


def pdf_dumper(file_lists, output_folder_path):
    # Create process bar
    file_lists_counter = process_bar_manager.counter(total=len(file_lists), desc='Total files process', unit='file',
                                                     color='green')
    file_lists_counter.refresh()

    # chunk list file
    if len(file_lists) < 3:
        chunked_list = list(map(lambda x: [x], file_lists))
    else:
        chunked_list = list(chunk_list(file_lists, 3))

    # init process pool
    executor = get_reusable_executor(max_workers=multiprocessing.cpu_count(), reuse=True)
    futures = {executor.submit(_process_work, chunk): chunk for chunk in chunked_list}

    for future in futures:
        try:
            future.result()
            file_lists_counter.update()
        except Exception as e:
            logger.error("Error: {} - {}", e, traceback.format_exc())

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
