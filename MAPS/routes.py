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


def get_patients():
    patients = requests.get(f"{API_URL}patients")
    json_data = json.loads(patients.text)

    list_id = []
    list_name = []

    for value in json_data:
        list_id.append(value['id'])
        list_name.append(f"{value['first_name']} {value['second_name']} {value['last_name']}")

    tuple_id_name = list(zip(list_id, list_name))
    return tuple_id_name


def get_doctors():
    doctors = requests.get(f"{API_URL}doctors")
    json_data = json.loads(doctors.text)

    list_id = []
    list_name = []

    for value in json_data:
        list_id.append(value['id'])
        list_name.append(f"Dr. {value['last_name']}")

    tuple_id_name = list(zip(list_id, list_name))
    return tuple_id_name

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
        patients = get_patients()
        form.patient_id.choices = patients

        doctors = get_doctors()
        form.doctor_id.choices = doctors

        if form.validate_on_submit():
            if request.method == 'POST':
                consultation = {"appointment": format_datetime_str(concat_date_time(form.date.data, form.start.data)),
                                "patient_id": form.patient_id.data,
                                "doctor_id": form.doctor_id.data,
                                "duration": str(CONSULTATION_DURATION),
                                "cause": form.reason.data,
                                "cancelled": form.cancelled.data
                                }
                print(consultation)
                URL = f"{API_URL}consultations"

                api_response = requests.post(url=URL, json=consultation)
                if api_response.status_code != 200:
                    google_calendar = gc_api()

                    index_reason = int(form.reason.data)
                    reason = form.reason.choices[index_reason][1]

                    index_doctor = int(form.doctor_id.data)
                    doctor = form.doctor_name.choices[index_doctor][1]

                    #  TODO Smarter way to transfer the chosen doctor to the calendar entry creation
                    write_text_file(PATH_DOCTOR, doctor)

                    title = f"Patient: {form.patient_name.data} Issue : {reason}"
                    date = concat_date_time(form.date.data, form.start.data)
                    google_event_id = google_calendar.insert_calendar_entry(title=title, date=date,
                                                                            patient_email="fightme1984@gmail.com",
                                                                            doctor_email="akbar.dakbar@shojiido.de",
                                                                            doctor=doctor, duration=CONSULTATION_DURATION)

                    flash(f'Appointment No. {google_event_id} with was successfully created!', 'success')

                    return redirect(url_for('calendar'))
                else:
                    flash(f'An Error happened, reason: {api_response.reason} please try again!', 'danger')
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
