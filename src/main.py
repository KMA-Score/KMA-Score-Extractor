from dhp.kma_score_extract import KMAScoreExtract
from dhp.db_import import DBImport
import os
import logging

logging.basicConfig(level=logging.INFO)

poppler_path = os.path.join(os.path.abspath(".."), "bin", "poppler-22.01.0", "Library", "bin")


def extract(file_path):
    temp_path = os.path.join(os.path.abspath(".."), "temp", "pdf2images_ppm")

    kma = KMAScoreExtract(file_path, poppler_path=poppler_path, temp_path=temp_path)

    kma_score = kma.extract()

    logging.info("Import to DB")

    db = DBImport(db_file="database.db")

    db.insert_into_db(kma_score)


if __name__ == "__main__":
    folder_path = os.path.join(os.path.abspath(".."), "sample")

    files_in_folder = os.listdir(folder_path)

    logging.info("Found {} file!".format(len(files_in_folder)))

    for file in files_in_folder:
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)

            extract(file_path)
