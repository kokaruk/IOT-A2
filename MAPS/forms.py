from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    secondname = StringField('Second Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth', format='%Y-%m-%d',
                    validators=[DataRequired()])
    gender = SelectField('Please select Gender',
                         choices=[('', 'Please select'), ('m', 'Male'), ('f', 'Female'), ('o', 'other')],
                         validators=[DataRequired()])
    address = TextAreaField('Address',
                            validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])

    phone = IntegerField('Telephone or Mobile',
                         validators=[DataRequired(), Length(min=1, max=9)])
    medicare = IntegerField('Medicare No',
                            validators=[DataRequired(), Length(min=1, max=9)])
    pre_conditions = TextAreaField('Previous Conditions')
    current_medications = TextAreaField('Current Medication')
    pre_doctor = StringField('Previous Doctor')
    pre_clinic = StringField('Previous Clinic')
    submit = SubmitField('Register')


class ConsultationForm(FlaskForm):
    start = DateField('Start of Consultation', format='%Y-%m-%d',
                      validators=[DataRequired()])
    end = DateField('End of Consultation', format='%Y-%m-%d',
                    validators=[DataRequired()])
    description = TextAreaField('Consultation description',
                                validators=[DataRequired()])
    additional_notes = TextAreaField('Current Medication')
    symptoms = TextAreaField('Symptoms')
    diagnosis = TextAreaField('Diagnosis')
    submit = SubmitField('Save Consultation Notes')
