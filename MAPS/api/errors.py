from flask import jsonify

from MAPS.api import bp


def bad_request():
    pass


@bp.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})
    response.status_code = 400
    return response
