import calendar
import time


def get_timestamp():
    current_local_time = time.localtime()

    time_stamp = calendar.timegm(current_local_time)

    return time_stamp
