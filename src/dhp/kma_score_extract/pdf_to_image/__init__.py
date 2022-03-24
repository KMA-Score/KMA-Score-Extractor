from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from tqdm import tqdm
import os
from pathlib import Path

default_temp_path = os.path.join(os.path.abspath(".."), "temp", "pdf2images")


def extract_image(filename, thread_count=3, poppler_path="", temp_path=None):
    if temp_path is None:
        temp_path = default_temp_path

    if not os.path.exists(temp_path):
        Path(temp_path).mkdir(parents=True, exist_ok=True)

    images = convert_from_path(filename, thread_count=thread_count, poppler_path=poppler_path)

    for i in tqdm(range(len(images))):
        images[i].save(os.path.join(temp_path, '{}.jpg'.format(i)), 'JPEG')
    pass

    return temp_path
