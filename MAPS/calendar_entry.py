"""
.. module:: MAPS.calendar_entry
    :synopsis: entering details to calendar

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from MAPS.constants import *
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http

from oauth2client import file, client, tools
from MAPS.utils import *
from flask import flash
import requests
import json

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
