import fitz
from tqdm import tqdm

from dhp_kma.core.spliter_pattern import *
from dhp_kma.utils.csv_reader import load_subject_mapping


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

    subject_mapping = load_subject_mapping()

    with fitz.open(pdf_file) as pages:
        # TODO: remove debugger
        # page = pages[97]
        # page_content = page.get_text()
        # print(page_content)
        #
        # exit(0)

        for i, page in enumerate(tqdm(pages)):
            page_content = page.get_text()

            global_subject_code = ""
            global_subject_name = ""

            if not page_content:
                continue

            page_content_line = page_content.split("\n")

            student_code_line = ""
            subject_noc = ""

            # loop to each line
            for pcl_index, x in enumerate(page_content_line):
                if x.__contains__('Mã học phần'):
                    student_code_line = x

                if x.__contains__('Số TC:'):
                    noc = pattern_noc(x, pcl_index, page_content_line)
                    if noc is not None:
                        subject_noc = noc

                if x.__contains__('Tên'):
                    sn = pattern_subject_name(pcl_index, page_content_line)

                    if sn is not None:
                        global_subject_name = sn
            # end of loop

            if not student_code_line:
                if not global_subject_code:  # Prevent cover and not score page
                    continue

                subject_code = global_subject_code  # Prevent page don't have subject code
            else:
                subject_code = student_code_line.split(":")[1].strip()
                global_subject_code = subject_code

            # in case subject name null check in subject_dict
            if global_subject_name is None or global_subject_name == "" or len(global_subject_name) <= 0:
                if subject_code in subject_dict.keys():
                    subject_data = next((item for item in subject_mapping if item["subjectCode"] == subject_code), None)

                    if subject_data is not None:
                        global_subject_name = subject_data.get('name', 'NULL')
                    else:
                        global_subject_name = "NULL"

            subject_dict[subject_code] = {
                'noc': subject_noc,
                'name': global_subject_name
            }

            if subject_code not in file_dict.keys():
                file_dict[subject_code] = [i]
            else:
                file_dict[subject_code].append(i)

    return file_dict, subject_dict
