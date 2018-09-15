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
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


class Google_Calendar_API:

    def call_api(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def insert_calandar(self):
        date = datetime.now()
        tomorrow = (date + timedelta(days=1)).strftime("%Y-%m-%d")
        time_start = "{}T06:00:00+10:00".format(tomorrow)
        time_end = "{}T07:00:00+10:00".format(tomorrow)
        event = {
            'summary': 'New Programmatic Event',
            'location': 'RMIT Building 14',
            'description': 'Adding new IoT event',
            'start': {
                'dateTime': time_start,
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': time_end,
                'timeZone': 'Australia/Melbourne',
            },
            'attendees': [
                {'email': 'kevin@scare.you'},
                {'email': 'shekhar@wake.you'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 5},
                    {'method': 'popup', 'minutes': 10},
                ],
            }
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: {}'.format(event.get('htmlLink')))
