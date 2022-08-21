from dhp.kma_score_extract import KMAScoreExtract
from dhp.db_import import DBImport
import os
import logging
import time

logging.basicConfig(level=logging.INFO)


def extract(path):
    logging.info("Scan folder for sample(s)")

    files_in_folder = [x for x in os.listdir(path) if x.endswith(".pdf")]

    logging.info("Found {} file(s)!".format(len(files_in_folder)))

    db = DBImport(db_file=os.path.join(os.path.abspath(".."), "output", "database.db"))
    # db = DBImport(db_file=os.path.join("C:\/Users\/phucp\/Desktop", "output", "database.db"))

    for file in files_in_folder:
        logging.info("Start File {}".format(file))

        file_path = os.path.join(path, file)

        kma = KMAScoreExtract(file_path)

        kma_scores, subject_dict = kma.extract()

        # TODO: Remove this. Use for Dev purpose only
        # print(kma_scores)

        logging.info("Import to DB")

        db.insert_into_db(kma_scores, subject_dict)


if __name__ == "__main__":
    tik = time.time()

    folder_path = os.path.join(os.path.abspath(".."), "sample")

    extract(folder_path)

    tok = time.time()

    logging.info("Process time: {:.2f} s".format(tok - tik))
