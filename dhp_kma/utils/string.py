import os
import sys
import importlib.resources


def clean_text(text):
    return str(text).strip()


def student_name_clean_text(text):
    return str(text).strip().replace("\n", " ")


def student_code_format(text):
    return clean_text(text).split(' ')[0]


def find_data_file(filename):
    datadir = importlib.resources.files("main")
    return os.path.join(str(datadir), "data", filename)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
