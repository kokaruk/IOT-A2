"""
.. module:: MAPS.api_connector
    :synopsis: accessing restful api

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
import requests
import json
from MAPS.constants import *


def get_user(user_type):
    """
    This methods purpose is to provide tuples of either doctor or patient id and name or id and name
    :param: user_type either 'patient' or 'doctor' expected
    :return: two tuples (<patient or doctor> id : <patient or doctor> name and <patient or doctor> id : <patient or doctor> email
    """

    if user_type == "patient":

        user = requests.get(f"{API_URL}patients")
    else:
        user = requests.get(f"{API_URL}doctors")

    # Turning json to list
    user_data = json.loads(user.text)

    list_id = []
    list_name = []
    list_email = []

    # extract the email, id and name to sperate list
    for value in user_data:
        list_id.append(value['id'])
        list_email.append(f"{value['email']}")
        if user_type == "patient":
            list_name.append(
                f"{value['first_name']} {value['second_name']} {value['last_name']}")

        else:
            list_name.append(f"Dr. {value['last_name']}")

    # join list together
    tuple_id_name = list(zip(list_id, list_name))
    tuple_id_emails = list(zip(list_id, list_email))

    return tuple_id_name, tuple_id_emails
