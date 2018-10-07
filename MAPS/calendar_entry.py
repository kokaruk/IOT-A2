"""
.. module:: MAPS.calendar_entry
    :synopsis: entering details to calendar

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from MAPS.constants import *

from oauth2client import file, client, tools
from MAPS.utils import format_datetime_str
from flask import flash
import requests
import json
from datetime import datetime

SCOPES_ADDRESS = 'https://www.googleapis.com/auth/calendar'
STORAGE = 'MAPS/credentials/token.json'
CLIENT_SECRETS = 'MAPS/credentials/google_calendar_api_credentials.json'
BUILD_DEF = 'calendar'
BUILD_NO = 'v3'

# If modifying these scopes, delete the file token.json.
SCOPES = SCOPES_ADDRESS
store = file.Storage(STORAGE)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRETS, SCOPES)
    creds = tools.run_flow(flow, store)
service = build(BUILD_DEF, BUILD_NO, http=creds.authorize(Http()))


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


def create_availability_entry(date_range, doctor_id):
    """
    Method for creating the entries of busy times
    :param date_range: has to be a dictionary of with ["start":Datetime, "end":Datetime]
    :param doctor_id: id of the doctor for this event
    """
    google_calendar = GoogleCalendarAPI()

    # Post data to Google Calendar API for event creation
    title = f"non-availability time"

    start = format_datetime_str(date_range["start"])
    end = format_datetime_str(date_range["end"])

    google_calendar.book_doctor_times(start=start, end=end, title=title, doctor_id=doctor_id)


class GoogleCalendarAPI:
    """ Purpose of this class is to manage the access calls to the google calendar API"""

    def insert_calendar_entry(self, title, date, patient_email, doctor_email, doctor_id, duration):
        """This method calls google API for creating Events based on the entries from the Users"
        :param title: String
        :param date: DateTime
        :param patient_email: String
        :param doctor_email: String
        :param doctor_id: Int
        :param duration: Int
        :return: google event_id (necessary if deletion is desired)
        """
        # Formatting times for appointment
        start = format_datetime_str(date)
        end = date + timedelta(minutes=duration)
        end = format_datetime_str(end)

        # building message body
        event = {
            'summary': title,
            'location': 'PoIT Medical, Collins Street 60, Melbourne 3000',
            'transparency': "opaque",
            'visibility': "private",
            'start': {
                'dateTime': str(start),
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': str(end),
                'timeZone': 'Australia/Melbourne',
            },
            'attendees': [
                {'email': str(patient_email)},
                {'email': str(doctor_email)}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 5},
                    {'method': 'popup', 'minutes': 10},
                ],
            }
        }
        try:
            doctor = requests.get(f"{API_URL}doctors")
            json_data = json.loads(doctor.text)
            for doctor in json_data:
                if doctor['id'] == doctor_id:
                    # sending the post recuest to google calendars
                    event = service.events().insert(calendarId=doctor["calendar_id"], body=event).execute()
                    print('Event created: {}'.format(event.get('htmlLink')))
                    # returning googles event id
                    return event.get('id')
        except Exception as err:
            # TODO better Exception handling
            print(err)

    def delete_calendar_entry(self, google_calendar_id, google_event_id):
        """
        Method for deleting an google calendar entry
        :param google_calendar_id: String
        :param google_event_id: String
        """
        # TODO Implement delete - issue how to get event ID
        try:
            delete = service.events().delete(calendarId=google_calendar_id, eventId=google_event_id).execute()
            if delete is None:
                flash(f'Event {event_id} sucessfully deleted', 'success')
            else:
                flash(f'Event {event_id} not deleted, reason: {delete.reason} please try again!', 'danger')
        except Exception as err:
            # TODO better Exception handling
            print(err)

    def book_doctor_times(self, start, end, title, doctor_id):
        """
        Similar to insert_calendar_entry method, it creates a event into the calendar but this is meant for busy times
        and marking availabilities
        :param start: Datetime
        :param end: DateTime
        :param title: String
        :param doctor_id: Int
        """
        # building message body
        event = {
            'summary': title,
            'transparency': "opaque",
            'visibility': "public",
            'start': {
                'dateTime': str(start),
                'timeZone': 'Australia/Melbourne'
            },
            'end': {
                'dateTime': str(end),
                'timeZone': 'Australia/Melbourne'
            }
        }
        try:
            doctor = requests.get(f"{API_URL}doctors")
            json_data = json.loads(doctor.text)
            for doctor in json_data:
                if doctor['id'] == doctor_id:
                    # sending the post recuest to google calendars
                    event = service.events().insert(calendarId=doctor["calendar_id"], body=event).execute()
                    print('Event created: {}'.format(event.get('htmlLink')))

                    return
        except Exception as err:
            # TODO better Exception handling
            print(err)
