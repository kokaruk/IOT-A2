#!/usr/bin/env python3
"""
* Authors : Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
*
* Version info 1.0.
*
* This program is created for Assignment 2 of Programming Internet of Things -  Course Master of IT - RMIT University.
* This code has parts which are inspired by the course material of  - Programming Internet of Things  - RMIT University.
*
* The purpose of the Program is to simulate an automated Medical Office..
* Booking of Consultations, Registration and Recording of Consultations Notes shall be managed via the MAPS Program
* For more information please see: https://github.com/kokaruk/IOT-A1.
*
* This Class shall manage the connection to Google Calendar API and let booking entries be send to Google API.
*
* Copyright notice - All copyrights belong to  Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from __future__ import print_function
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from MAPS.utils import format_datetime_str

# TODO Find a better way to store constants.
DOC1 = 'cvrsdsk7jjae29p9fg9t6vcr94@group.calendar.google.com'
DOC2 = 'co63bbo22htf8jqombkb2tguh8@group.calendar.google.com'
DOC3 = '9kn05ti5cef5mt9kcpup4sjt4g@group.calendar.google.com'

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


class Google_Calendar_API:

    def insert_calendar_entry(self, title, date, patient_email, doctor_email, doctor, duration):

        start = format_datetime_str(date)
        end = date + timedelta(minutes=duration)
        end = format_datetime_str(end)

        event = {
            'summary': title,

            'location': 'PoIT Medical, Collins Street 60, Melbourne 3000',
            'description': 'Adding new IoT event',
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
            if doctor == "Dr Akbar Dakbar":
                # TODO Exchange CalendarID with DB entry of CalendarID
                event = service.events().insert(calendarId=DOC1, body=event).execute()
                print('Event created: {}'.format(event.get('htmlLink')))
            elif doctor == "Dr Gerry Skinner":
                event = service.events().insert(calendarId=DOC2, body=event).execute()
                print('Event created: {}'.format(event.get('htmlLink')))
            else:
                event = service.events().insert(calendarId=DOC3, body=event).execute()
                print('Event created: {}'.format(event.get('htmlLink')))
        except Exception as err:
            # TODO better Exceptionhandleing
            print(err)

    def delete_calendar_entry(self, calendar_id='primary', event_id='eventId'):
        """NOT READY YET """
        # TODO Implement delete - issue how to get event ID
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
