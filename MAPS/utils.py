"""
.. module:: MAPS.utils
    :synopsis: Flask error handling

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from datetime import datetime
from MAPS.calendar_entry import GoogleCalendarAPI as gc_api
from MAPS.constants import *


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


def create_availability_entry(date_range, doctor_id):
    """
    Method for creating the entries of busy times
    :param date_range: has to be a dictionary of with ["start":Datetime, "end":Datetime]
    :param doctor_id: id of the doctor for this event
    """
    google_calendar = gc_api()

    # Post data to Google Calendar API for event creation
    title = f"non-availability time"

    start = format_datetime_str(date_range["start"])
    end = format_datetime_str(date_range["end"])

    google_calendar.book_doctor_times(start=start, end=end, title=title, doctor_id=doctor_id)


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


def build_default_busy_times(doctor_id, year, week):
    """
    Method for building the default time where doctors is not working(busy as per google calendar entry)
    These times are Saturday and Sunday entirely and Monday to Friday 00:00 - 7:59 (morning), Lunch Break (12:31 - 13:29)
    and evening (17:31 - 23:59)
    :param doctor_id: doctor_id: id of the doctor for this event
    :param year: %Y format of year (2018)
    :param week: format %W (1-52)

    """
    for weekdays in WEEKDAYS:

        if weekdays == "saturday" or weekdays == "sunday":
            start = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 00:00", "%Y-%W-%w %H:%M")
            end = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 23:59", "%Y-%W-%w %H:%M")

            weekend_times = dict({"start": start, "end": end})

            create_availability_entry(weekend_times, doctor_id)

        else:
            start_morning = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 00:00", "%Y-%W-%w %H:%M")
            end_morning = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 07:59", "%Y-%W-%w %H:%M")

            morning = dict({"start": start_morning, "end": end_morning})

            create_availability_entry(morning, doctor_id)

            start_break = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 12:31", "%Y-%W-%w %H:%M")
            end_break = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 13:29", "%Y-%W-%w %H:%M")

            break_time = dict({"start": start_break, "end": end_break})

            create_availability_entry(break_time, doctor_id)

            start_evening = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 17:31", "%Y-%W-%w %H:%M")
            end_evening = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 23:59", "%Y-%W-%w %H:%M")

            evening = dict({"start": start_evening, "end": end_evening})

            create_availability_entry(evening, doctor_id)
