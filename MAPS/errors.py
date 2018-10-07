"""
.. module:: MAPS.errors
    :synopsis: Flask error handling

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob

flask server error handling
"""

from flask import render_template
from MAPS import app, db


@app.errorhandler(404)
def not_found_error(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    return render_template('500.html'), 500
