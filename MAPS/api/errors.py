from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from MAPS.api import bp


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request():
    return error_response(400, "An error occurred")


@bp.errorhandler(400)
def custom400(error):
    return error_response(400, error.description)
