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
* This file has a set of useful methods that are used throughout the program.
*
* Copyright notice - All copyrights belong to  Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from datetime import datetime


def write_text_file(path, entry):
    try:
        with open(path,'w') as w:
            w.write(entry)
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Write Error")

def read_text_file(path):
    """Reads txt file and returns a variable"""
    try:
        with open(path,'r') as r:
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
    """formates a datetime to string as YYYY-MM-DDTH:M:S"""
    date_time_formatted = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    return date_time_formatted
