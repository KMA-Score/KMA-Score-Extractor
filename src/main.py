from dhp.kma_score_extract import KMAScoreExtract
import os

FILENAME = "test.pdf"
poppler_path = os.path.join(os.path.abspath(".."), "bin", "poppler-22.01.0", "Library", "bin")
tesseract_path = r'E:\PROJECT\KMA\iKMA\pdfScanner\bin\tesseract\windows\tesseract.exe'

if __name__ == "__main__":
    file_path = os.path.join(os.path.abspath(".."), "sample", FILENAME)

    kma = KMAScoreExtract(file_path, poppler_path=poppler_path, tesseract_path=tesseract_path)

    kma_score = kma.extract()

    print(kma_score)
