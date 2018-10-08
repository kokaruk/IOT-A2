#!/usr/bin/env python3
"""
.. module:: run
    :synopsis: Main Runner class.

.. moduleauthor:: Dzmitry Kakaruk
.. moduleauthor:: Calvin Schnierer
.. moduleauthor:: Patrick Jacob

Primary runner module. Provide access to run app from cli.
"""

from app import app

if __name__ == '__main__':
    app.run()
