"""
.. module:: MAPS.utils
    :synopsis: Flask error handling

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
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
