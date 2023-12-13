from dhp_kma.utils.string import is_number


def pattern_noc(x, pcl_index, page_content_line):
    subject_noc = None

    # Số TC: 3
    # Mã học phần: DT1DVDM8
    if page_content_line[pcl_index + 1].__contains__('Mã học phần'):
        split_subject_noc = x.split(":")

        if len(split_subject_noc) > 1:
            subject_noc = split_subject_noc[1].strip()

    # Số TC:
    # 3
    # Mã học phần: DT1DVDM8
    elif page_content_line[pcl_index + 2].__contains__('Mã học phần'):
        subject_noc = page_content_line[pcl_index + 1]

    return subject_noc


def _process_subject_name(name):
    split_name = name.split("-")
    n = str(split_name[0])
    n = n.strip()  # remove leading and trailing spaces
    n = n.replace('"', '')  # remove double quotes
    return n


def pattern_subject_name(pcl_index, page_content_line):
    global_subject_name = None
    total_index = len(page_content_line) - 1

    # patterns

    # Tên
    # HỌC VIỆN KỸ THUẬT MẬT MÃ
    #  HỌC KỲ 1 NĂM HỌC 2019_2020
    # Giáo dục thể chất 1 - AT16
    # CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    if total_index >= (pcl_index + 4) and page_content_line[pcl_index + 1].__contains__(
            'HỌC VIỆN KỸ THUẬT MẬT MÃ') and page_content_line[pcl_index + 4].__contains__(
        'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'):
        global_subject_name = page_content_line[pcl_index + 3]

    # PHÒNG KT&ĐBCLĐT
    # KẾT QUẢ ĐIỂM HỌC PHẦN
    # Tên
    # HỌC VIỆN KỸ THUẬT MẬT MÃ
    #  HỌC KỲ 1 NĂM HỌC 2019_2020
    # Toán cao cấp A3 - AT16
    elif total_index >= (pcl_index + 3) and page_content_line[pcl_index - 1].__contains__(
            'KẾT QUẢ ĐIỂM HỌC PHẦN') and page_content_line[pcl_index + 1].__contains__('HỌC VIỆN KỸ THUẬT MẬT MÃ'):
        global_subject_name = page_content_line[pcl_index + 3]

    # PHÒNG KT&ĐBCLĐT
    # KẾT QUẢ ĐIỂM HỌC PHẦN
    # Tên
    # Tin học đại cương - AT16
    # HỌC VIỆN KỸ THUẬT MẬT MÃ
    elif page_content_line[pcl_index - 1].__contains__('KẾT QUẢ ĐIỂM HỌC PHẦN'):
        global_subject_name = page_content_line[pcl_index + 1]

    # CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    # HỌC VIỆN KỸ THUẬT MẬT MÃ
    # KẾT QUẢ ĐIỂM HỌC PHẦN (Thi lại)
    # Hệ điều hành nhúng thời gian thực - CT4DT3
    # Tên
    elif page_content_line[pcl_index - 2].__contains__('KẾT QUẢ ĐIỂM HỌC PHẦN'):
        global_subject_name = page_content_line[pcl_index - 1]

    elif page_content_line[pcl_index - 2].__contains__('Ghi chú'):
        global_subject_name = page_content_line[pcl_index - 1]

    elif page_content_line[pcl_index - 1].__contains__('Ghi chú'):
        global_subject_name = page_content_line[pcl_index + 1]

    elif total_index >= pcl_index + 1 and page_content_line[pcl_index - 1].__contains__('HỌC KỲ'):
        global_subject_name = page_content_line[pcl_index + 1]

    # KẾT QUẢ ĐIỂM HỌC PHẦN
    # CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    # Độc lập - Tự do - Hạnh phúc
    # PHÒNG KT&ĐBCLĐT
    # Hà Nội,  ngày 10 tháng 6 năm 2022
    #  HỌC KỲ 1 NĂM HỌC 2021_2022 (Thi lại)
    # Cơ sở an toàn và bảo mật thông tin - CT3
    # Tên
    elif page_content_line[pcl_index - 6].__contains__('CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'):
        global_subject_name = page_content_line[pcl_index - 1]

    # Hệ điều hành nhúng thời gian thực - CT3
    # Tên
    # HỌC VIỆN KỸ THUẬT MẬT MÃ
    # CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    # PHÒNG KT&ĐBCLĐT
    elif total_index >= pcl_index + 2 and page_content_line[pcl_index + 1].__contains__(
            'HỌC VIỆN KỸ THUẬT MẬT MÃ') and page_content_line[pcl_index + 2].__contains__(
        'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'):
        global_subject_name = page_content_line[pcl_index - 1]

    # Hệ điều hành nhúng thời gian thực - CT3
    # Tên
    # Hà Nội,  ngày 13 tháng 6 năm 2022
    # HỌC VIỆN KỸ THUẬT MẬT MÃ
    # CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    elif total_index >= pcl_index + 2 and page_content_line[pcl_index + 2].__contains__('HỌC VIỆN KỸ THUẬT MẬT MÃ'):
        global_subject_name = page_content_line[pcl_index - 1]

    elif total_index >= pcl_index + 3 and page_content_line[pcl_index + 3].__contains__('HỌC VIỆN KỸ THUẬT MẬT MÃ'):
        global_subject_name = page_content_line[pcl_index + 1]

    if global_subject_name is not None and is_number(global_subject_name):
        return None

    # process final result
    if global_subject_name is not None:
        global_subject_name = _process_subject_name(global_subject_name)

    return global_subject_name
