from flask import render_template, url_for, flash, redirect, request
from MAPS.forms import RegistrationForm, ConsultationDetailsForm, BookingForm, ConsultationBookings, \
    ScheduleBookingForm, ConsultationForm
from MAPS import app
from MAPS.utils import concat_date_time, read_text_file, format_datetime_str
from MAPS.calendar_entry import GoogleCalendarAPI as gc_api
import requests
import json
from datetime import timedelta, datetime
import socket
# reference: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/25850698#25850698
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip_address = s.getsockname()[0]
API_URL = f"http://{local_ip_address}:5000/api/"

CONSULTATION_DURATION = 20
PATH_DOCTOR = "MAPS/credentials/doctor.txt"
# base_url = request.host_url
FORMAT_JSON_DATE_STRING = '%Y-%m-%dT%H:%M:%S%z'

# Choices for selection field - why a patient wants to visit the clinc (should be basis for scheduling optimization
choices_reason = [('0', 'Please select'), ('1', 'Pick up a prescription'), ('2', 'Serious illness - e.g. flu'),
                  ('3', 'Medical exam'), ('4', 'Vaccination'), ('5', 'Pick up a medical certificate'), ('0', 'unknown')]


# TODO REFACTOR EVERYTHING!!!

def get_user(user_type):
    """This methods purpose is to provide tubles of either doctor or patient id and name or id and name"""
    if user_type == "patient":

        user = requests.get(f"{API_URL}patients")
    else:
        user = requests.get(f"{API_URL}doctors")

    # Turning json to list
    user_data = json.loads(user.text)

    list_id = []
    list_name = []
    list_email = []

    # extract the email, id and name to sperate list
    for value in user_data:
        list_id.append(value['id'])
        list_email.append(f"{value['email']}")
        if user_type == "patient":
            list_name.append(
                f"{value['first_name']} {value['second_name']} {value['last_name']}")

        else:
            list_name.append(f"Dr. {value['last_name']}")

    # join list together
    tuple_id_name = list(zip(list_id, list_name))
    tuple_id_emails = list(zip(list_id, list_email))

    return tuple_id_name, tuple_id_emails


@app.route("/")
@app.route("/home")
def home():
    """Rendering homepage"""
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    """Rendering about page"""
    return render_template('about.html', title='About')


@app.route("/patient")
def patient():
    """Rendering welcome page for patients"""
    return render_template('patient.html', title='Patient')


@app.route("/clerk")
def clerk():
    """Rendering welcome page for clerks"""
    return render_template('clerk.html', title='Clerk')


@app.route("/doctor")
def doctor():
    """Rendering welcome page for doctor"""
    return render_template('doctor.html', title='Doctor')


def get_work_time(daytime, year, week, day):
    morning_start = "08:00"
    morning_end = "12:30"

    afternoon_start = "13:00"
    afternoon_end = "18:30"

    weekday = dict({"monday": 1, "tuesday": 2, "wednesday": 3,
                    "thursday": 4, "friday": 5})

    if daytime == "morning":
        start = datetime.strptime(
            f"{year}-{week}-{weekday[day]} {morning_start}", "%Y-%W-%w %H:%M")
        end = datetime.strptime(
            f"{year}-{week}-{weekday[day]}  {morning_end}", "%Y-%W-%w %H:%M")
    else:
        start = datetime.strptime(
            f"{year}-{week}-{weekday[day]} {afternoon_start}", "%Y-%W-%w %H:%M")
        end = datetime.strptime(
            f"{year}-{week}-{weekday[day]}  {afternoon_end}", "%Y-%W-%w %H:%M")

    from_to = dict({"start": start, "end": end})

    return from_to


@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    """Rendering Schedule Page for weekly schedule of doctors"""
    form = ScheduleBookingForm()
    doctors = get_user("doctor")

    year = form.year.data

    week = form.calendar_week.data

    if form.monday_morning.data:
        monday_morning_times = get_work_time("morning", year, week, 'monday')
    if form.monday_afternoon.data:
        monday_afternoon_times = get_work_time(
            "afternoon", year, week, 'monday')
    if form.tuesday_morning.data:
        tuesday_morning_times = get_work_time("morning", year, week, 'tuesday')
    if form.tuesday_afternoon.data:
        tuesday_afternoon_times = get_work_time(
            "afternoon", year, week, 'tuesday')
    if form.wednesday_morning.data:
        wednesday_morning_times = get_work_time(
            "morning", year, week, 'wednesday')
    if form.wednesday_afternoon.data:
        wednesday_afternoon_times = get_work_time(
            "afternoon", year, week, 'wednesday')
    if form.thursday_morning.data:
        thursday_morning_times = get_work_time(
            "morning", year, week, 'thursday')
    if form.thursday_afternoon.data:
        thursday_afternoon_times = get_work_time(
            "afternoon", year, week, 'thursday')
    if form.friday_morning.data:
        friday_morning_times = get_work_time("morning", year, week, 'friday')
    if form.friday_afternoon.data:
        friday_afternoon_times = get_work_time(
            "afternoon", year, week, 'friday')

    # TODO Find a way to store globally
    doctors_id_name = doctors[0]  # contains tuples of doctor id and names

    # passing the tuples for doctor over to forms for access on View
    form.doctor_id.choices = doctors_id_name

    schedule_dict = {"doctor_id": form.doctor_id.data}

    return render_template('schedule.html', title='Schedule', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Rendering patient registration page and post to database API """
    try:
        form = RegistrationForm()
        if form.validate_on_submit():

            # building the message body as dictionary based on the forms entry
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

                # post the patient registration to DateBase API
                api_response = requests.post(url=URL, json=patient_dict)

                if api_response.status_code == 200:
                    flash('Your registration was sucessful', 'success')
                    return redirect(url_for('booking'))
                else:
                    flash(
                        f'Your registration failed, reason: {api_response.reason} please try again!', 'danger')
                return redirect(url_for('register'))
        return render_template('patient_register.html', title='Register', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/consultation_list", methods=['GET', 'POST'])
def consultation_list():
    """Shall open a possibility to """
    form = ConsultationForm()

    # TODO Find a way to store globally
    doctors = get_user("doctor")
    doctors_id_name = doctors[0]  # contains tuples of doctor id and names
    form.doctor_id.choices = doctors_id_name

    chosen_doctor_id = form.doctor_id.data

    if chosen_doctor_id == None:
        # initially the first doctor select field is shown
        consultations = requests.get(f"{API_URL}consultations/doctors/3")
    else:
        # with every choice of doctor and hit search the booking with the choosen doctor is shown
        consultations = requests.get(
            f"{API_URL}consultations/doctors/{chosen_doctor_id}")

    bookings = json.loads(consultations.text)

    # Bringing json string of date to datetime
    for booking in bookings:
        booking_date = booking['appointment']
        booking['appointment'] = datetime.strptime(
            booking_date, FORMAT_JSON_DATE_STRING)
        # Adding an end time for it
        booking['appointment_end'] = booking['appointment'] + \
            timedelta(minutes=CONSULTATION_DURATION)

    return render_template('consultation_list.html', title='Consultation Bookings List', form=form,
                           bookings=bookings, doctors_name=dict(doctors_id_name))


@app.route("/consultation/<consultation_id>", methods=['GET', 'POST', 'PUT'])
def consultation(consultation_id):
    # TODO Test if this works
    """Rendering patient consultation details page and post to database API """
    try:
        form = ConsultationDetailsForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                # building the message body as dictionary based on the forms entry
                consultation_details = {"consultation_id": consultation_id,
                                        "description": form.description.data,
                                        "additional_notes": form.additional_notes.data,
                                        "symptoms": form.symptoms.data,
                                        "diagnosis": form.diagnosis.data,
                                        "actual_start": format_datetime_str(
                                            concat_date_time(form.date.data, form.start.data)),
                                        "actual_end": format_datetime_str(
                                            concat_date_time(form.date.data, form.end.data))
                                        }
                URL = f"{API_URL}consultations/details"

                # post the consultation to DateBase API
                api_response = requests.post(
                    url=URL, json=consultation_details)

                if api_response.status_code == 200:
                    flash('Consultation was successfully saved!', 'success')
                    return redirect(url_for('consultation_list'))
                else:
                    flash(
                        f'An Error happened, reason: {api_response.reason} please try again!', 'danger')
                return redirect(url_for('consultation_list'))
        return render_template('consultation_details.html', title='Consultation', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/booking", methods=['GET', 'POST'])
# TODO get POST Method to POST to API
def booking():
    """Rendering consultation booking page and post to database API and to google calender method """
    try:
        form = BookingForm()

        # TODO Find a way to store globally
        # getting a list of patient_id and name tuples for the dynamic selectfield
        patients = get_user("patient")
        # contains tuples of patient id and names
        patients_id_name = patients[0]
        # contains tuples of patient id and emails
        patients_id_email = patients[1]

        # passing the tuples for patient over to forms for access on View
        form.patient_id.choices = patients_id_name

        # gettig a list of doctorid and name tuples for the dynamic selectfield
        doctors = get_user("doctor")
        # TODO Find a way to store globally
        doctors_id_name = doctors[0]  # contains tuples of patient id and names
        # contains tuples of patient id and emails
        doctors_id_email = doctors[1]

        # passing the tuples for doctor over to forms for access on View
        form.doctor_id.choices = doctors_id_name

        # getting a list of doctorid and name tuples for the dynamic selectfield
        form.reason.choices = choices_reason

        if form.validate_on_submit():
            if request.method == 'POST':

                # instatiating google API class
                google_calendar = gc_api()

                # retrieve the selected doctor and patient id from forms
                chosen_doctor_id = form.doctor_id.data
                chosen_patient_id = form.patient_id.data

                # retrieve the selected reason for visit
                index_reason = int(form.reason.data)
                reason = form.reason.choices[index_reason][1]

                patient_name = dict(patients_id_name)[chosen_patient_id]
                doctor_email = dict(doctors_id_email)[chosen_doctor_id]
                patient_email = dict(patients_id_email)[chosen_patient_id]

                if form.create.data is True:
                    # Post data to Google Calendar API for event creation
                    title = f"Patient: { patient_name } Issue : {reason}"
                    date = concat_date_time(form.date.data, form.start.data)
                    google_event_id = google_calendar.insert_calendar_entry(title=title, date=date,
                                                                            patient_email=patient_email,
                                                                            doctor_email=doctor_email,
                                                                            doctor_id=chosen_doctor_id,
                                                                            duration=CONSULTATION_DURATION)

                    # Building Message Body for database post request
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

                    # post the calendar entry to DateBase API
                    api_response = requests.post(url=URL, json=consultation)
                    if api_response.status_code != 200:
                        flash(
                            f'An Error happened, reason: {api_response.reason} please try again!', 'danger')
                        return redirect(url_for('calendar'))
                    else:
                        flash(f'Appointment with google event no. {google_event_id} with was successfully created!',
                              'success')
                elif form.delete.data is True:
                    flash(f'Appointment', 'success')
            return redirect(url_for('consultation_list'))
        return render_template('booking_create.html', title='Consultation Booking', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/calendar")
def calendar():
    """Posting and rendering embedded google calender API  """
    # TODO needs overwork to post the correct calendar API
    doctor = read_text_file(PATH_DOCTOR)

    return render_template('calendar.html', title='calendar', doctor=doctor)


@app.route("/statistics")
def statistics():
    """Posting and rendering embedded google statistics from datastudio """
    # TODO needs overwork on time series
    return render_template('statistics.html', title='statistics')


@app.route("/consultation_booking/<int:booking_id>")
def consultation_booking(booking_id):
    """show to singular booking content for clerk to overview or to cancel if necessary"""

    booking = requests.get(f"{API_URL}consultations/{booking_id}")
    consultation_booking = json.loads(booking.text)

    # Bringing json string of date to datetime
    consultation_booking['appointment'] = datetime.strptime(consultation_booking['appointment'],
                                                            FORMAT_JSON_DATE_STRING)
    # Adding an end time for it
    consultation_end = consultation_booking['appointment'] + \
        timedelta(minutes=CONSULTATION_DURATION)

    # TODO Find a way to store globally
    doctors = get_user("doctor")
    doctors_id_name = doctors[0]

    # TODO Find a way to store globally
    patients = get_user("patient")
    patients_id_name = patients[0]

    # TODO Better way to show date time
    return render_template('booking_show.html', title='Consultation Booking', booking=consultation_booking,
                           cause=dict(choices_reason),
                           doctor_name=dict(doctors_id_name), patient_name=dict(patients_id_name), end=consultation_end)


@app.route("/consultation_bookings", methods=['POST', 'GET'])
def consultation_bookings():
    """ Showing the list of all consultation bookings - filter by doctor"""

    form = ConsultationBookings()

    # TODO Find a way to store globally
    doctors = get_user("doctor")
    doctors_id_name = doctors[0]  # contains tuples of doctor id and names
    form.doctor_id.choices = doctors_id_name

    chosen_doctor_id = form.doctor_id.data

    if chosen_doctor_id == None:
        # initially the first doctor select field is shown
        consultation_bookings = requests.get(
            f"{API_URL}consultations/doctors/3")
    else:
        # with every choice of doctor and hit search the booking with the choosen doctor is shown
        consultation_bookings = requests.get(
            f"{API_URL}consultations/doctors/{chosen_doctor_id}")

    bookings = json.loads(consultation_bookings.text)

    # Bringing json string of date to datetime
    for booking in bookings:
        booking_date = booking['appointment']
        booking['appointment'] = datetime.strptime(
            booking_date, FORMAT_JSON_DATE_STRING)
        # Adding an end time for it
        booking['appointment_end'] = booking['appointment'] + \
            timedelta(minutes=CONSULTATION_DURATION)

    # TODO Find a way to store globally
    patients = get_user("patient")
    patients_id_name = patients[0]

    # TODO Better way to show date time
    return render_template('booking_list.html', title='Consultation Bookings List', form=form,
                           bookings=bookings, doctors_name=dict(doctors_id_name), patients_name=dict(patients_id_name),
                           cause=dict(choices_reason))


@app.route("/delete_booking/<int:booking_id>", methods=['GET', 'PUT'])
def cancel_booking(booking_id):
    """show to singular booking content for clerk to overview or to set cancel if necessary"""

    URL = f"{API_URL}consultations/{booking_id}"
    mark_booking_cancelled = {
        "cancelled": True
    }
    # Send PUT request to database API for booking (its not delete - only a marking it cancelled
    api_response = requests.put(url=URL, json=mark_booking_cancelled)
    if api_response.status_code != 200:
        flash(
            f'An Error happened, reason: {api_response.reason} please try again!', 'danger')
        # return redirect(url_for('consultation_booking', booking_id = booking_id))
    else:
        flash(f'Appointment with google event no. {google_event_id} with was successfully created!',
              'success')

    # TODO make doctor ID somehow global and draw from there values
    booking = requests.get(f"{API_URL}consultations/{booking_id}")
    consultation_booking = json.loads(booking.text)

    # getting event_id from booking
    doctor_id = dict(consultation_booking)["doctor_id"]
    google_event_id = dict(consultation_booking)["google_event_id"]

    # Getting the google Calendar ID which is attached to doctor
    doctor = requests.get(f"{API_URL}doctors/{doctor_id}")
    doctor = json.loads(doctor.text)
    google_calendar_id = dict(doctor)["calendar_id"]

    google_calendar = gc_api()
    # Calling delete method for google calendar entry (event)
    google_calendar.delete_calendar_entry(google_calendar_id, google_event_id)

    return redirect(url_for('consultation_booking', booking_id=booking_id))
