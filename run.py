#!/usr/bin/env python3
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
*
* Copyright notice - All copyrights belong to  Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from MAPS import app

db = SQLAlchemy()
migrate = Migrate()

if __name__ == '__main__':
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from MAPS.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.run(debug=True)
