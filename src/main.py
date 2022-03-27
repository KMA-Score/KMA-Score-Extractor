from dhp.kma_score_extract import KMAScoreExtract
from dhp.db_import import DBImport
import os
import logging
import time

logging.basicConfig(level=logging.INFO)

poppler_path = os.path.join(os.path.abspath(".."), "bin", "poppler-22.01.0", "Library", "bin")


def extract(file_path):
    temp_path = os.path.join(os.path.abspath(".."), "temp", "pdf2images_ppm")

    kma = KMAScoreExtract(file_path, poppler_path=poppler_path, temp_path=temp_path)

    kma_score, subject_dict = kma.extract()

    # TODO: Remove this. Use for Dev purpose only
    # print(kma_score)

    db = DBImport(db_file=os.path.join(os.path.abspath(".."), "output", "database_new.db"))

    logging.info("Import to DB")

    db.insert_into_db(kma_score, subject_dict)


if __name__ == "__main__":
    tic = time.time()

    folder_path = os.path.join(os.path.abspath(".."), "sample")

    files_in_folder = [x for x in os.listdir(folder_path) if x.endswith(".pdf")]

    logging.info("Found {} file!".format(len(files_in_folder)))

    for file in files_in_folder:
        logging.info("Start File {}".format(file))
        file_path = os.path.join(folder_path, file)

        extract(file_path)

    toc = time.time()

    logging.info("Process time: {} s".format(toc - tic))
