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
        w = open(path, "w")
        w.write(entry)
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Write Error")
    return


def read_text_file(path):
    """Reads text file and returns a variable"""
    try:
        content = open("path", "r")
        return content
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Write Error")


def concat_date_time(date, time, set_string_format):
    """Reads text file and returns a variable"""
    if set_string_format:
        date_time = datetime.combine(date, time)
        date_time_mel_format = date_time.strftime("%Y-%m-%dT%H:%M:%S+10")
        return date_time_mel_format
    else:
        date_time = datetime.combine(date, time)
        return date_time
