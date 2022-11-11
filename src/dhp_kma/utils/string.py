def clean_text(text):
    return str(text).strip()


def student_name_clean_text(text):
    return str(text).strip().replace("\n", " ")


def student_code_format(text):
    return clean_text(text).split(' ')[0]
