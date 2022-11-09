from loguru import logger

from kma.core.subject_spliter import subject_spliter


class KmaScoreCore:
    def __init__(self, filePath):
        logger.info("Init Kma Score Core")
        self.file_path = filePath
        pass

    def run(self):
        file_dict, subject_dict = subject_spliter(self.file_path)

        print(file_dict)
        print(subject_dict)
