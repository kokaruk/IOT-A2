#!/usr/bin/env python3
"""
.. module:: run
    :synopsis: Main Runner class.

.. moduleauthor:: Dzmitry Kakaruk
.. moduleauthor:: Calvin Schnierer
.. moduleauthor:: Patrick Jacob

Primary runner module. Provide access to run app from cli.
"""

from MAPS import app
from MAPS.models import *


@app.shell_context_processor
def make_shell_context():
    """
    Establish context of app to cli
    :returns: json of cli identifiers, callable from flask shell
    """
    return {'db': db, 'Patient': Patient, 'Doctor': Doctor}


if __name__ == '__main__':
    from MAPS.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.run(debug=True)
