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
import datetime


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    secondname = StringField('Second Name', validators=[Length(max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Please select Gender',
                         choices=[('', 'Please select'), ('m', 'Male'), ('f', 'Female'), ('o', 'other')],
                         validators=[DataRequired()])
    address = TextAreaField('Address',
                            validators=[DataRequired()])
    email = EmailField(label="Email",
                       render_kw={"placeholder": "name@email.com",
                                  "pattern": "^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"},
                       validators=[DataRequired(), Email()])
    phone = TelField('Telephone or Mobile',
                     render_kw={
                         "placeholder": "04 XXXX XXXX",
                     "pattern": "^(\(04\)|04|\+614)([ ]?\d){8}$"},
                     validators=[DataRequired()])
    medicare = StringField('Medicare No',
                           validators=[Length(min=9, max=10, message="Medicare No. has to be 10 digits"),
                                       DataRequired()])
    pre_conditions = TextAreaField('Previous Conditions')
    current_medications = TextAreaField('Current Medication')
    pre_doctor = StringField('Previous Doctor')
    pre_clinic = StringField('Previous Clinic')
    submit = SubmitField('Register')


class ConsultationForm(FlaskForm):
    doctor_id = SelectField('Please select doctors', choices=[], coerce=int, default=(1, 'Dr. Parker'))
    patient_id = SelectField('Please select patient', choices=[], coerce=int)
    date = DateField('Consultation Date', default=datetime.datetime.today())
    search = SubmitField('Search Appointments')


class ConsultationDetailsForm(FlaskForm):
    # TODO pre fill information from booking
    date = DateField('Consultation Date',
                     validators=[DataRequired()])
    start = TimeField('Start of Consultation', format='%H:%M',
                      validators=[DataRequired()])
    end = TimeField('End of Consultation', format='%H:%M',
                    validators=[DataRequired()])
    description = TextAreaField('Consultation description',
                                validators=[DataRequired()])
    symptoms = TextAreaField('Symptoms')
    diagnosis = TextAreaField('Diagnosis')
    additional_notes = TextAreaField('Additional Notes')
    submit = SubmitField('Save Consultation Notes')


class BookingForm(FlaskForm):
    date = DateField('Consultation Date', validators=[DataRequired()])
    start = TimeField('Consulation Time', format='%H:%M',
                      validators=[DataRequired()])
    patient_id = SelectField('Please select patient', choices=[], coerce=int, validators=[InputRequired()])
    doctor_id = SelectField('Please select doctors', choices=[], coerce=int, validators=[InputRequired()])
    reason = SelectField('Please select reason for doctors visit', choices=[], coerce=int, validators=[DataRequired()])
    cancelled = BooleanField('Cancelled Appointment')

    create = SubmitField('Book Consultation')
    delete = SubmitField('Delete Consultation')


class ConsultationBookings(FlaskForm):
    doctor_id = SelectField('Please select doctors', choices=[], coerce=int, default=(1, 'Dr. Parker'))
    search = SubmitField('Search Consultations')


class ScheduleBookingForm(FlaskForm):
    now = datetime.datetime.now()
    doctor_id = SelectField('Please select doctors', choices=[], coerce=int, validators=[InputRequired()])
    year = StringField('Please choose year', default=f"{now.year}")
    calendar_week = StringField('Please choose year',
                                default=datetime.date(now.year, now.month, now.day).strftime("%V"))
    monday_morning = BooleanField('Monday Morning')
    monday_afternoon = BooleanField('Monday Afternoon')
    tuesday_morning = BooleanField('Tuesday Morning')
    tuesday_afternoon = BooleanField('Tuesday Afternoon')
    wednesday_morning = BooleanField('Wednesday Morning')
    wednesday_afternoon = BooleanField('Wednesday Afternoon')
    thursday_morning = BooleanField('Thursday Morning')
    thursday_afternoon = BooleanField('Thursday Afternoon')
    friday_morning = BooleanField('Friday Morning')
    friday_afternoon = BooleanField('Friday Afternoon')
    create_week = SubmitField('Book Availabilites')
