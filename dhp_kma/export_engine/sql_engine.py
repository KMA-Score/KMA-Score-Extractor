import csv
import os.path
from tqdm import tqdm
from loguru import logger


def sql_gen(input_path, output_path):
    # get file extension of one of the file in input folder
    file_extension = None

    if os.path.exists(os.path.join(input_path, "score.tsv")) is True:
        file_extension = "tsv"
    elif os.path.exists(os.path.join(input_path, "score.csv")) is True:
        file_extension = "csv"
    else:
        raise Exception("Can't find source file")

    global delimiter
    delimiter = "\t" if file_extension == "tsv" else ","

    score_path = os.path.join(input_path, f"score.{file_extension}")
    student_path = os.path.join(input_path, f"student.{file_extension}")
    subject_path = os.path.join(input_path, f"subject.{file_extension}")

    ref_output_path = input_path if output_path is None else output_path

    score_output_path = os.path.join(ref_output_path, "output", "score.sql")
    student_output_path = os.path.join(ref_output_path, "output", "student.sql")
    subject_output_path = os.path.join(ref_output_path, "output", "subject.sql")

    # ensure output folder exist
    os.makedirs(os.path.dirname(score_output_path), exist_ok=True)

    _generate_sql_score(score_path, score_output_path)
    _generate_sql_student(student_path, student_output_path)
    _generate_sql_subject(subject_path, subject_output_path)


def _generate_sql_score(input_path, output_path):
    logger.info("Generating SQL command...")

    sql_array = []

    # read csv file
    with open(input_path, encoding='utf-8') as f:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(f, delimiter=delimiter)

        # convert each csv row into python dict
        for row in tqdm(list(csv_reader)):
            sql_command = "INSERT INTO Scores (" \
                          "StudentId," \
                          "SubjectId," \
                          "FirstComponentScore," \
                          "SecondComponentScore," \
                          "ExamScore," \
                          "AvgScore," \
                          "AlphabetScore) " \
                          "VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\") " \
                          "ON DUPLICATE KEY UPDATE " \
                          "FirstComponentScore=\"{}\"," \
                          "SecondComponentScore=\"{}\"," \
                          "ExamScore=\"{}\"," \
                          "AvgScore=\"{}\"," \
                          "AlphabetScore=\"{}\";".format(row["StudentId"], row["SubjectId"], row["FirstComponentScore"],
                                                         row["SecondComponentScore"], row["ExamScore"], row["AvgScore"],
                                                         row["AlphabetScore"], row["FirstComponentScore"],
                                                         row["SecondComponentScore"], row["ExamScore"], row["AvgScore"],
                                                         row["AlphabetScore"])

            sql_array.append(sql_command)

    with open(output_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write("\n".join(sql_array))


def _generate_sql_student(input_path, output_path):
    logger.info("Generating SQL command...")

    sql_array = []

    # read csv file
    with open(input_path, encoding='utf-8') as f:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(f, delimiter=delimiter)

        # convert each csv row into python dict
        for row in tqdm(list(csv_reader)):
            sql_command = "INSERT INTO Students (" \
                          "Id," \
                          "Name," \
                          "Class) " \
                          "VALUES (\"{}\",\"{}\",\"{}\") " \
                          "ON DUPLICATE KEY UPDATE " \
                          "Name=\"{}\"," \
                          "Class=\"{}\";".format(row["Id"], row["Name"], row["Class"], row["Name"], row["Class"])

            sql_array.append(sql_command)

    with open(output_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write("\n".join(sql_array))


def _generate_sql_subject(input_path, output_path):
    logger.info("Generating SQL command...")

    sql_array = []

    # read csv file
    with open(input_path, encoding='utf-8') as f:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(f, delimiter=delimiter)

        # convert each csv row into python dict
        for row in tqdm(list(csv_reader)):
            sql_command = "INSERT INTO Subjects (" \
                          "Id," \
                          "Name," \
                          "NumberOfCredits) " \
                          "VALUES (\"{}\",\"{}\",\"{}\") " \
                          "ON DUPLICATE KEY UPDATE " \
                          "Name=\"{}\"," \
                          "NumberOfCredits=\"{}\";".format(row["Id"], row["Name"], row["NumberOfCredits"], row["Name"],
                                                           row["NumberOfCredits"])

            sql_array.append(sql_command)

    with open(output_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write("\n".join(sql_array))
