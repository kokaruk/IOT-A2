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
from wtforms import DateTimeField
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

akbars_calendar = '6qu20tinkidnvhcg7snr19aqvc@group.calendar.google.com'
gerrys_calendar = '1vp7utbb9quuha30ho09lf5j0o@group.calendar.google.com'

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('MAPS/credentials/token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('MAPS/credentials/google_calendar_api_credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


class Google_Calendar_API:

    def insert_calendar_entry(self, title, date, patient_email, patient, doctor_email, doctor, duration):

        start_time = (date - timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%S+10")
        end_time = (date - timedelta(hours=10) + timedelta(minutes=duration)).strftime("%Y-%m-%dT%H:%M:%S+10")

        event = {
            'summary': title,

            'location': 'PoIT Medical, Collins Street 60, Melbourne 3000',
            'description': 'Adding new IoT event',
            'start': {
                'dateTime': str(start_time),
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': str(end_time),
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
        if doctor == "Dr Akbar Dakbar":
            event = service.events().insert(calendarId=akbars_calendar, body=event).execute()
            print('Event created: {}'.format(event.get('htmlLink')))
        else:
            event = service.events().insert(calendarId=gerrys_calendar, body=event).execute()
            print('Event created: {}'.format(event.get('htmlLink')))

    def delete_calandar_entry(self, calendar_id='primary', event_id='eventId'):

        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
