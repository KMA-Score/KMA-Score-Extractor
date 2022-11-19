import sys

from dhp_kma.core import KmaScoreCore
from dhp_kma.export_engine.csv_engine import CsvEngine
from dhp_kma.utils.command_line import *
from dhp_kma.utils.sanity_check import *
from dhp_kma.utils.time_utils import *

if __name__ == "__main__":
    args, parser = create_command_line()

    if args.type is None:
        parser.print_help()

    if args.type == "dump":
        PATH = args.path
        log_level = args.debug

        logger.remove()

        if log_level is True:
            logger.add(sys.stderr, level="DEBUG")
        else:
            logger.add(sys.stderr, level="INFO")

        sanity_check()

        if args.output_path:
            OUTPUT_PATH = args.output_path
        else:
            OUTPUT_PATH = os.path.join(os.path.abspath("."), "output/output-score-{}.csv".format(get_timestamp()))

        obj = os.scandir(PATH)

        file_list = []

        for entry in obj:
            if entry.is_file():
                file_list.append(entry)

        logger.info("Found {file} files!", file=len(file_list))

        export_engine = CsvEngine(file_path=OUTPUT_PATH)

        for file_name in file_list:
            handler = KmaScoreCore(os.path.join(os.path.abspath("."), "sample", file_name))
            subject_dict, file_score_data = handler.run()

            export_engine.run_score(file_score_data)

        export_engine.close_file()
