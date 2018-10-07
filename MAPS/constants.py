"""
.. module:: MAPS.constants
    :synopsis: Package global constants

.. moduleauthor:: Dzmitry Kakaruk
.. moduleauthor:: Calvin Schnierer
.. moduleauthor:: Patrick Jacob

A neat way to collect and manage all the package globals
"""
# routes constants
CONSULTATION_DURATION = 20
PATH_DOCTOR = "MAPS/credentials/doctor.txt"
FORMAT_JSON_DATE_STRING = '%Y-%m-%dT%H:%M:%S%z'
API_URL = "http://127.0.0.1:5000/api/"
WEEKDAYS = dict({"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 0})