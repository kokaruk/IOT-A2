from flask import render_template, url_for, flash, redirect, request
from MAPS.forms import RegistrationForm, ConsultationForm, BookingForm
from MAPS import app
from MAPS.utils import concat_date_time, write_text_file, read_text_file, format_datetime_str
from MAPS.calendar_entry import GoogleCalendarAPI as gc_api
import requests
import json

CONSULTATION_DURATION = 20
PATH_DOCTOR = "MAPS/credentials/doctor.txt"
API_URL = "http://127.0.0.1:5000/api/"


def get_user(user_type):
    if user_type == "patient":

        user = requests.get(f"{API_URL}patients")
    else:
        user = requests.get(f"{API_URL}doctors")

    json_data = json.loads(user.text)

    list_id = []
    list_name = []
    list_email = []

    for value in json_data:
        list_id.append(value['id'])
        list_email.append(f"{value['email']}")
        if user_type == "patient":
            list_name.append(f"{value['first_name']} {value['second_name']} {value['last_name']}")
        else:
            list_name.append(f"Dr. {value['last_name']}")

    tuple_id_name = list(zip(list_id, list_name))
    tuple_emails = list(zip(list_id, list_email))

    return tuple_id_name, tuple_emails

@app.route("/")
@app.route("/home")
def home():
    """Rendering homepage"""
    return render_template('home.html')


@app.route("/about")
def about():
    """Rendering about page"""
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Rendering patient registration page and post to database API """
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                patient_dict = {"first_name": form.firstname.data,
                                "second_name": form.secondname.data,
                                "last_name": form.lastname.data,
                                "dob": format_datetime_str(form.dob.data),
                                "gender": form.gender.data,
                                "address": form.address.data,
                                "email": form.email.data,
                                "phone": form.phone.data,
                                "medicare_number": form.medicare.data,
                                "previous_doctor": form.pre_doctor.data,
                                "current_medication:": form.current_medications.data,
                                "previous_clinic": form.pre_clinic.data
                                }

                URL = f"{API_URL}patients"
                api_response = requests.post(url=URL, json=patient_dict)
                if api_response.status_code == 200:
                    flash('Your registration was sucessful', 'success')
                    return redirect(url_for('booking'))
                else:
                    flash(f'Your registration failed, reason: {api_response.reason} please try again!', 'danger')
                return redirect(url_for('register'))
        return render_template('patient_register.html', title='Register', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/consultation", methods=['GET', 'POST'])
def consultation():
    """Rendering patient consultation details page and post to database API """
    try:
        form = ConsultationForm()
        if form.validate_on_submit():
            if request.method == 'POST':

                consultation_details = {"description": form.description.data,
                                        "additional_notes": form.additional_notes.data,
                                        "symptoms": form.symptoms.data,
                                        "diagnosis": form.diagnosis.data,
                                        "actual_start": format_datetime_str(
                                            concat_date_time(form.date.data, form.start.data)),
                                        "actual_end": format_datetime_str(
                                            concat_date_time(form.date.data, form.end.data))
                                        }
                URL = f"{API_URL}consultations/details"
                api_response = requests.post(url=URL, json=consultation_details)
                if api_response.status_code == 200:
                    flash('Consultation was successfully saved!', 'success')
                    return redirect(url_for('consultation'))
                else:
                    flash(f'An Error happened, reason: {api_response.reason} please try again!', 'danger')
                return redirect(url_for('consultation'))
        return render_template('consultation.html', title='Consultation', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/booking", methods=['GET', 'POST'])
# TODO get POST Method to POST to API
def booking():
    """Rendering consultation booking page and post to database API and to google calender method """
    try:
        form = BookingForm()
        patients = get_user("patient")
        patients_id_name = patients[0]  # contains tuples of patient id and names
        patients_id_email = patients[1]  # contains tuples of patient id and emails

        form.patient_id.choices = patients_id_name

        doctors = get_user("doctor")
        doctors_id_name = doctors[0]  # contains tuples of patient id and names
        doctors_id_email = doctors[1]  # contains tuples of patient id and emails

        form.doctor_id.choices = doctors_id_name

        if form.validate_on_submit():
            if request.method == 'POST':

                google_calendar = gc_api()

                chosen_doctor_id = form.doctor_id.data
                chosen_patient_id = form.patient_id.data

                index_reason = int(form.reason.data)
                reason = form.reason.choices[index_reason][1]

                patient_name = dict(patients_id_name)[chosen_patient_id]
                doctor_email = dict(doctors_id_email)[chosen_doctor_id]
                patient_email = dict(patients_id_email)[chosen_patient_id]

                if form.create.data is True:
                    title = f"Patient: { patient_name }Issue : {reason}"
                    date = concat_date_time(form.date.data, form.start.data)
                    google_event_id = google_calendar.insert_calendar_entry(title=title, date=date,
                                                                            patient_email=patient_email,
                                                                            doctor_email=doctor_email,
                                                                            doctor_id=chosen_doctor_id,
                                                                            duration=CONSULTATION_DURATION)

                    consultation = {
                        "appointment": format_datetime_str(concat_date_time(form.date.data, form.start.data)),
                        "patient_id": chosen_patient_id,
                        "doctor_id": chosen_doctor_id,
                        "duration": str(CONSULTATION_DURATION),
                        "cause": form.reason.data,
                        "cancelled": form.cancelled.data,
                        'google_event_id': google_event_id
                        }
                    print(consultation)

                    URL = f"{API_URL}consultations"

                    api_response = requests.post(url=URL, json=consultation)
                    if api_response.status_code != 200:
                        flash(f'An Error happened, reason: {api_response.reason} please try again!', 'danger')
                        return redirect(url_for('calendar'))
                    else:
                        flash(f'Appointment with google event no. {google_event_id} with was successfully created!',
                              'success')
                elif form.delete.data is True:
                    flash(f'Appointment', 'success')
            return redirect(url_for('consultation'))
        return render_template('booking.html', title='Consultation Booking', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/calendar")
def calendar():
    """Posting google calender API  """
    doctor = read_text_file(PATH_DOCTOR)

    return render_template('calendar.html', title='calendar', doctor=doctor)
