import csv
from tqdm import tqdm


def generate_sql_score(input_path, output_path):
    sql_array = []

    # read csv file
    with open(input_path, encoding='utf-8') as f:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(f)

        # convert each csv row into python dict
        for row in tqdm(csv_reader):
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


def generate_sql_student(input_path, output_path):
    sql_array = []

    # read csv file
    with open(input_path, encoding='utf-8') as f:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(f)

        # convert each csv row into python dict
        for row in tqdm(csv_reader):
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


def generate_sql_subject(input_path, output_path):
    sql_array = []

    # read csv file
    with open(input_path, encoding='utf-8') as f:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(f)

        # convert each csv row into python dict
        for row in tqdm(csv_reader):
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
