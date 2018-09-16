from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)], default="John")
    secondname = StringField('Second Name', validators=[Length(max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)], default="Smith")
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Please select Gender',
                         choices=[('', 'Please select'), ('m', 'Male'), ('f', 'Female'), ('o', 'other')],
                         validators=[DataRequired()])
    address = TextAreaField('Address',
                            validators=[DataRequired()], default="2012 Main Street, 3423 Central City ")
    email = EmailField(label="Email", validators=[DataRequired(), Email()], default="john.smith@hotmail.com")
    phone = TelField('Telephone or Mobile',
                     validators=[DataRequired()])
    medicare = StringField('Medicare No',
                           validators=[Length(min=9, max=10, message="Medicare No. has to be 10 digits"),
                                       DataRequired()], default=1234567890)
    pre_conditions = TextAreaField('Previous Conditions')
    current_medications = TextAreaField('Current Medication')

    # Test with FieldList for 1 to N fields - issue is it doesn't dynamically grow - stay at min entries
    # pre_conditions = FieldList(StringField('Previous Conditions'), min_entries=1, max_entries=10)
    # current_medications = FieldList(TextAreaField('Current Medication'), min_entries=1, max_entries=10)

    pre_doctor = StringField('Previous Doctor')
    pre_clinic = StringField('Previous Clinic')
    submit = SubmitField('Register')


class ConsultationForm(FlaskForm):
    date = DateField('Consulation Date',
                     validators=[DataRequired()])
    start = TimeField('Start of Consultation', format='%H:%M',
                      validators=[DataRequired()])
    end = TimeField('End of Consultation', format='%H:%M',
                    validators=[DataRequired()])
    description = TextAreaField('Consultation description',
                                validators=[DataRequired()])
    additional_notes = TextAreaField('Additional Notes')
    symptoms = TextAreaField('Symptoms')
    diagnosis = TextAreaField('Diagnosis')

    submit = SubmitField('Save Consultation Notes')


class BookingForm(FlaskForm):
    date = DateField('Consultation Date', validators=[DataRequired()])
    start = TimeField('Consulation Time', format='%H:%M',
                      validators=[DataRequired()])
    patient_name = StringField('Patient Name',
                               validators=[DataRequired(), Length(min=2, max=20)], default="John Smith")
    doctor_name = SelectField('Please select reason for doctors Visit',
                              choices=[('', 'Please select'), ('1', 'Dr Akbar Dakbar'),
                                       ('2', 'Dr Gerry Skinner')], validators=[DataRequired()])
    reason = SelectField('Please select reason for doctors Visit',
                         choices=[('', 'Please select'), ('1', 'Pick up a prescription'),
                                  ('2', 'Serious illness - e.g. flu'),
                                  ('3', 'Medical exam'), ('4', 'Vaccination'), ('5', 'Pick up a medical certificate'),
                                  ('0', 'unknown')], validators=[DataRequired()])
    cancelled = BooleanField('Cancelled Appointment')

    submit = SubmitField('Book Consultation')
