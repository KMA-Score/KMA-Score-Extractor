from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from tqdm import tqdm
import os
import tempfile


def extract_image(filename, thread_count=3, poppler_path=""):
    # temp_folder =
    temp_folder = os.path.join(os.path.abspath(".."), "temp", "pdf2images")

    images = convert_from_path(filename, thread_count=thread_count, poppler_path=poppler_path)

    for i in tqdm(range(len(images))):
        # images[i].save('temp/pdfImage/' + str(i) + '.jpg', 'JPEG')
        images[i].save(os.path.join(temp_folder, '{}.jpg'.format(i)), 'JPEG')
    pass

    return temp_folder
