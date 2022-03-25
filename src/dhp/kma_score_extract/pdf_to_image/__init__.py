from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import os
from pathlib import Path

default_temp_path = os.path.join(os.path.abspath(".."), "temp", "pdf2images_ppm")


def extract_image(filename, thread_count=8, poppler_path="", temp_path=None):
    """
    Extract image from pdf using pdf2image
    :param filename: Path to file
    :type filename str
    :param thread_count: Number of thread use to extract (Default: 8)
    :type thread_count int
    :param poppler_path: Path to poppler_path if not installed in PATH
    :type poppler_path str
    :param temp_path: Path to save temp file
    :type temp_path str
    :return: List of PIL image
    :rtype: list
    """
    if temp_path is None:
        temp_path = default_temp_path

    if not os.path.exists(temp_path):
        Path(temp_path).mkdir(parents=True, exist_ok=True)

    images = convert_from_path(filename, dpi=400, thread_count=thread_count, poppler_path=poppler_path,
                               output_folder=temp_path)

    return images
