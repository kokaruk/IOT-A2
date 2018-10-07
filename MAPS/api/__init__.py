"""
.. module:: MAPS.api
    :synopsis: Package, contains modules with calls to database

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""

from flask import Blueprint

bp = Blueprint('api', __name__)

from MAPS.api import patients, doctors, consultations, errors
