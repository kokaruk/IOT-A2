#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import sys
import json
import socket
import datetime
import requests
import dateutil.parser

from google.assistant.library.event import EventType
import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip_address = s.getsockname()[0]
API_URL = "http://{}:5000/api/".format(local_ip_address)
GRPC_URL = ""

PATIENT_ENDPOINT = "patients"
CONSULTATION_ENDPOINT = "consultations/"
CONSULTATION_FOR_PATIENT_ENDPOINT = "{}patients/".format(
    CONSULTATION_ENDPOINT)
DETAILS = "details"
CONSULTATION_DETAILS_ENDPOINT = "consultations/{}/".format(DETAILS)


previous_intent = ''
selected_patient = {}
selected_day = {}
selected_consultation = {}
field = ''


def convert(time_string):
    """
    Accepts a datetime string in the format YYYY-MM-DDTHH-mm-ss+00:00
    :param time_string datetime as a string:
    :return: datetime
    """
    return datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')


def responder(assistant, response):
    """
    Accpets an assistant instance, and a response. Prints the response, says the response with the assistant, and starts
    a conversation to listen to next voice command.
    :param assistant:
    :param String response:
    """
    print(response)
    aiy.audio.say(response)
    assistant.start_conversation()


def get_patients(speak):
    """
    Returns list of registered patients. Will read them out if True is passed.
    :param Bool speak:
    :return: JSON array of users
    """
    print("--------------")
    print("get_patients()")
    print("Getting registered patients")
    users = requests.get("{}{}".format(API_URL, PATIENT_ENDPOINT))
    users_data = json.loads(users.text)
    if speak:
        aiy.audio.say(
            "You have {} registered patients".format(len(users_data)))
        print("You have {} registered patients".format(len(users_data)))
        for user in users_data:
            aiy.audio.say("{} {}".format(
                user['first_name'], user['last_name']))
            print("{} {}".format(user['first_name'], user['last_name']))
    return users_data


def get_consultations(patient):
    """
    Returns all consultations for the provided patient.
    :param JSON object patient:
    :return: JSON array of consultations
    """
    print("--------------")
    print("get_consultation()")
    print("Getting consultation for patient")
    request_url = "{}{}{}".format(
        API_URL, CONSULTATION_FOR_PATIENT_ENDPOINT, patient['id'])
    consultations = requests.get(request_url)
    return json.loads(consultations.text)


def add_consultation_note_who(assistant):
    """
    Prompts doctor for patient's first name.
    Accepts an assistant, to pass to the responder.
    :param assistant:
    :return: String of this intent name
    """
    print("--------------")
    print("add_consultation_note_who")
    response = 'Sure, who is this for?'
    responder(assistant, response)
    return 'add_consultation_note_who'


def add_consultation_note_patient(assistant, text):
    """
    Searches list of registered patients against previous response.
    If there's a match, prompts for day.
    :param assistant:
    :param previous response as String text:
    :return: JSON object of patient if match or empty if no match
    """
    global previous_intent
    global selected_patient
    print("--------------")
    print("add_consultation_note_patient")
    print("previous_intent was add_consultation_note_who")
    patients = get_patients(False)
    for patient in patients:
        if patient['first_name'].lower() == text.lower():
            print("{} matches {}".format(text, patient['first_name']))
            response = "Found {}. What day?".format(text)
            responder(assistant, response)
            return patient
    response = "Sorry there is no one by the name of {}".format(text)
    responder(assistant, response)
    return {}


def add_consultation_note_day(assistant, text):
    """
    Converts Today, Yesterday etc... into datetimes and checks against the consultation list.
    Currently only today is supported.
    :param assistant:
    :param previous response as String text:
    :return: JSON object of matched consultation of empty object.
    """
    global previous_intent
    global selected_patient
    global selected_day
    global selected_consultation
    global field
    print("--------------")
    print("add_consultation_notes_field")
    print("previous_intent was add_consultation_note_patient")
    if 'today' in text:
        consultations = get_consultations(selected_patient)
        now = datetime.datetime.today()
        for consultation in consultations:
            date_time = dateutil.parser.parse(consultation['appointment'])
            if now.day == date_time.day:
                response = "Found consultation. What would you like to update?"
                responder(assistant, response)
                return consultation
        response = "No consultation found"
        responder(assistant, response)
    else:
        response = "Sorry, only today is supported"
        responder(assistant, response)
    return {}


def add_consultation_note_field(assistant, text):
    """
    Prompts doctor to record note.
    Sets the global variable field to previous response, which is the consultation details field to be updated.
    :param assistant:
    :param previous response as String text:
    :return: String field
    """
    global previous_intent
    global field
    field = text
    response = 'Please dictate your note'
    responder(assistant, response)
    previous_intent = 'add_consultation_note_field'
    return field


def record_note(assistant, text):
    """
    Updates consultation details with recorded note.
    :param assistant:
    :param previous response as String text:
    :return: True if success, False if unsuccessful.
    """
    global field
    global selected_consultation
    consultation_detail = selected_consultation['consultation_details'][0]
    if field == 'diagnosis':
        consultation_detail['diagnosis'] = text
        print(consultation_detail)
    if field == 'condition':
        consultation_detail['condition'] = text
        print(consultation_detail)
    if field == 'description':
        consultation_detail['description'] = text
        print(consultation_detail)
    if field == 'symptoms':
        consultation_detail['symptoms'] = text
        print(consultation_detail)
    url = "{}{}{}".format(API_URL, CONSULTATION_DETAILS_ENDPOINT,
                          consultation_detail['id'])
    print("Sending update")
    api_response = requests.put(url=url, json=consultation_detail)
    if api_response.status_code == 200:
        response = "You've updated the {}".format(field)
        responder(assistant, response)
        return True
    else:
        response = 'An error occurred, note has not been recorded'
        responder(assistant, response)
        print(api_response)
        return False


def process_event(assistant, event):
    """
    Modified function - added custom intents to record consultation details via conversation.
    :param assistant:
    :param event:
    """
    global previous_intent
    global selected_patient
    global selected_day
    global selected_consultation
    global field
    print("----------------------------")
    print("assistant: " + str(assistant))
    print("event: " + str(event.type))
    print("previous_intent: " + previous_intent)
    status_ui = aiy.voicehat.get_status_ui()

    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if 'stop' in text:
            assistant.stop_conversation()
            previous_intent = ''
        elif 'exit' in text:
            assistant.stop_conversation()
            sys.exit(1)
        elif 'get registered patients' in text or 'get registered patience' in text:
            assistant.stop_conversation()
            get_patients(True)
        # Doctor wants to add a note
        elif 'add note' in text or 'at note' in text:
            assistant.stop_conversation()
            previous_intent = add_consultation_note_who(assistant)
        # Find out which patient the consultation note is for
        elif previous_intent == 'add_consultation_note_who':
            assistant.stop_conversation()
            patient = add_consultation_note_patient(assistant, text)
            if patient == {}:
                previous_intent = ''
            else:
                previous_intent = 'add_consultation_note_patient'
                selected_patient = patient
        # Find out what day the consultation was only - only today supported currently
        elif previous_intent == 'add_consultation_note_patient':
            assistant.stop_conversation()
            consultation = add_consultation_note_day(assistant, text)
            if consultation == {}:
                previous_intent = ''
            else:
                previous_intent = 'add_consultation_note_day'
                selected_consultation = consultation
        # Find out which note field to update
        elif previous_intent == 'add_consultation_note_day':
            assistant.stop_conversation()
            add_consultation_note_field(assistant, text)
        # Record the note
        elif previous_intent == 'add_consultation_note_field':
            assistant.stop_conversation()
            record_note(assistant, text)
            previous_intent = ''
            selected_patient = {}
            selected_day = {}
            selected_consultation = {}
            field = ''

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    global API_URL
    # get the IP address of your Raspberry Pi running MAPS api
    api = input(
        "Enter your api's IP address or press enter if running on host: ")
    if api != '':
        API_URL = "http://{}:5000/api/".format(api)
    print("API URL: {}".format(API_URL))

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        print(assistant._model_id)  # voice-app-iot-voice-kit
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
