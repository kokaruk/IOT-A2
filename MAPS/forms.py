from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField, TelField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, InputRequired


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
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    phone = TelField('Telephone or Mobile',
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
    # TODO pre fill information from booking
    date = DateField('Consulation Date',
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
    reason = SelectField('Please select reason for doctors Visit',
                         choices=[('', 'Please select'), ('1', 'Pick up a prescription'),
                                  ('2', 'Serious illness - e.g. flu'),
                                  ('3', 'Medical exam'), ('4', 'Vaccination'), ('5', 'Pick up a medical certificate'),
                                  ('0', 'unknown')], validators=[DataRequired()])
    cancelled = BooleanField('Cancelled Appointment')

    create = SubmitField('Book Consultation')
    delete = SubmitField('Delete Consulation')
