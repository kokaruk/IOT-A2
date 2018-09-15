from flask import Blueprint

bp = Blueprint('api', __name__)

from MAPS.api import patients, doctors, consultations, consultationDetails, errors
