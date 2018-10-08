"""
.. module:: MAPS.forms
    :synopsis: WTF form module

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob

Various information capturing forms present in the project
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField, TelField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, InputRequired


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Confirm')
