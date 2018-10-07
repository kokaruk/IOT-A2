"""
.. module:: MAPS.utils
    :synopsis: Flask error handling

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from MAPS.constants import *
from datetime import datetime

def write_text_file(path, entry):
    try:
        with open(path, 'w') as w:
            w.write(entry)
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Write Error")


def read_text_file(path):
    """Reads txt file and returns a variable"""
    try:
        with open(path, 'r') as r:
            content = r.read()
        return content
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Write Error")


def concat_date_time(date, time):
    """concatenates a date and time to datetime object"""
    date_time = datetime.combine(date, time)
    return date_time


def format_datetime_str(date_time):
    """formats a datetime to string as YYYY-MM-DDTH:M:S"""
    date_time_formatted = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    return date_time_formatted





def get_work_time(daytime, year, week, day):
    """
    This is a helper method for taking the week and weekday and cast to a datetime format for further processing
    :param daytime: Either "morning" or "afternoon"
    :param year: %Y format of year (2018)
    :param week: format %W (1-52)
    :param day: String (one of "monday" - "friday")
    :return: dict with two datetime 8start to end )
    """
    morning_start = "08:00"
    morning_end = "12:30"

    afternoon_start = "13:00"
    afternoon_end = "18:30"

    if daytime == "morning":
        start = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]} {morning_start}", "%Y-%W-%w %H:%M")
        end = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]}  {morning_end}", "%Y-%W-%w %H:%M")
    else:
        start = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]} {afternoon_start}", "%Y-%W-%w %H:%M")
        end = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]}  {afternoon_end}", "%Y-%W-%w %H:%M")

    from_to = dict({"start": start, "end": end})

    return from_to
