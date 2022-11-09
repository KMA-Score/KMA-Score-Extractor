import fitz
import json
from tqdm import tqdm
import os


def subject_spliter(pdf_file):
    """
    Divide page by subject
    :param pdf_file: Path to PDF file
    :type pdf_file str
    :return: Dictionary of SubjectCode-Page Mapping
     :rtype: dict
    """
    file_dict = {}
    subject_dict = {}

    global_subject_code = ""

    with fitz.open(pdf_file) as pages:
        with open(os.path.join(os.path.join('data'), 'subjectNameMapping.json'), encoding="utf-8") as f:
            subject_mapping = json.loads(f.read())

        for i, page in enumerate(tqdm(pages)):
            page_content = page.get_text()

            if not page_content:
                continue

            page_content_line = page_content.split("\n")

            student_code_line = ""
            subject_noc = ""

            for pcl_index, x in enumerate(page_content_line):
                if x.__contains__('Mã học phần'):
                    student_code_line = x

                if x.__contains__('Số TC:'):
                    subject_noc = page_content_line[pcl_index + 1]

            if not student_code_line:
                if not global_subject_code:  # Prevent cover and not score page
                    continue

                subject_code = global_subject_code  # Prevent page don't have subject code
            else:
                subject_code = student_code_line.split(":")[1].strip()
                global_subject_code = subject_code

            if subject_code not in subject_dict.keys():
                subject_data = next((item for item in subject_mapping if item["subjectCode"] == subject_code), None)

                if subject_data is not None:
                    subject_name = subject_data.get('name', 'NULL')
                else:
                    subject_name = "NULL"

                subject_dict[subject_code] = {
                    'noc': subject_noc,
                    'name': subject_name
                }

            if subject_code not in file_dict.keys():
                file_dict[subject_code] = [i]
            else:
                file_dict[subject_code].append(i)

    return file_dict, subject_dict
