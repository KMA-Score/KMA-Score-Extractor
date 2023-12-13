from loguru import logger

from dhp_kma.core.subject_spliter import subject_spliter
from dhp_kma.core.extract_pdf_table import extract_table


class KmaScoreCore:
    def __init__(self, file_path):
        logger.info("Init Kma Score Core...")
        logger.info("Handle file path {path}", path=file_path)

        self.file_path = file_path

    def run(self):
        # Load subject - page mapping
        subject_name_page_mapping, subject_dict = subject_spliter(self.file_path)

        logger.info("Found {length_file_dict} subjects!", length_file_dict=len(subject_name_page_mapping))
        logger.debug(subject_name_page_mapping)
        logger.debug(subject_dict)

        # Start extract page
        file_score_data = extract_table(self.file_path, subject_name_page_mapping)

        logger.debug(file_score_data)

        return subject_dict, file_score_data
