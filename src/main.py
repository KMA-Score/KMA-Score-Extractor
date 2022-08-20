from dhp.kma_score_extract import KMAScoreExtract
from dhp.db_import import DBImport
import os
import logging
import time

logging.basicConfig(level=logging.INFO)


def extract(path):
    kma = KMAScoreExtract(path)

    kma_scores = kma.extract()

    # TODO: Remove this. Use for Dev purpose only
    # print(kma_scores)

    # db = DBImport(db_file=os.path.join(os.path.abspath(".."), "output", "database_with_name.db"))

    logging.info("Import to DB")

    # db.insert_into_db(kma_score, subject_dict)


if __name__ == "__main__":
    tik = time.time()

    folder_path = os.path.join(os.path.abspath(".."), "sample")

    extract(folder_path)

    tok = time.time()

    logging.info("Process time: {:.2f} s".format(tok - tik))
