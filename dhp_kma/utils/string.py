import os
import sys


def clean_text(text):
    return str(text).strip()


def student_name_clean_text(text):
    return str(text).strip().replace("\n", " ")


def student_code_format(text):
    return clean_text(text).split(' ')[0]


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, "../../", "data", filename)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
