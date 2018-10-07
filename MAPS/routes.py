from flask import render_template, url_for, flash, redirect, request
from MAPS.forms import RegistrationForm, ConsultationDetailsForm, BookingForm, ConsultationBookings, \
    ScheduleBookingForm, ConsultationForm
from MAPS import app
from MAPS.utils import concat_date_time, read_text_file, format_datetime_str
from MAPS.calendar_entry import GoogleCalendarAPI as gc_api
import requests
import json
from datetime import timedelta, datetime
import MAPS.constants as config

API_URL = "http://127.0.0.1:5000/api/"
# base_url = request.host_url

# Choices for selection field - why a patient wants to visit the clinc (should be basis for scheduling optimization)
CHOICES_REASON = [(0, 'Please select'), (1, 'Pick up a prescription'), (2, 'Serious illness - e.g. flu'),
                  (3, 'Medical exam'), (4, 'Vaccination'), (5, 'Pick up a medical certificate')]

WEEKDAYS = dict({"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 0})

def get_user(user_type):
    """
    This methods purpose is to provide tuples of either doctor or patient id and name or id and name
    :param: user_type either 'patient' or 'doctor' expected
    :return: two tuples (<patient or doctor> id : <patient or doctor> name and <patient or doctor> id : <patient or doctor> email
    """

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
    """
    Route to home page for rending view
    :return: render_template with home.html
    """
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    """
    Route to about page for rending view
    :return: render_template with about.html
    """
    return render_template('about.html', title='About')


@app.route("/patient")
def patient():
    """
    Route to patient start page for rending view
    :return: render_template with patient.html
    """
    return render_template('patient.html', title='Patient')


@app.route("/clerk")
def clerk():
    """
    Route to patient start page for rending view
    :return: render_template with clerk.html
    """
    return render_template('clerk.html', title='Clerk')


@app.route("/doctor")
def doctor():
    """
    Route to doctors start page for rending view
    :return: render_template with clerk.html
    """
    return render_template('doctor.html', title='Doctor')


def get_work_time(daytime, year, week, day):
    """
    This is a helper method for taking the week and weekday and cast to a datetime format for further processing
    :param daytime: Either "morning" or "afternoon"
    :param year: %Y format of year (2018)
    :param week: format %W (1-52)
    :param day: String (one of "monday" - "friday")
    :return: dict with two datetime 8start to end )
    """
    morning_start = "08:00"
    morning_end = "12:30"

    afternoon_start = "13:00"
    afternoon_end = "18:30"

    if daytime == "morning":
        start = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]} {morning_start}", "%Y-%W-%w %H:%M")
        end = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]}  {morning_end}", "%Y-%W-%w %H:%M")
    else:
        start = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]} {afternoon_start}", "%Y-%W-%w %H:%M")
        end = datetime.strptime(
            f"{year}-{week}-{WEEKDAYS[day]}  {afternoon_end}", "%Y-%W-%w %H:%M")

    from_to = dict({"start": start, "end": end})

    return from_to


def build_default_busy_times(doctor_id, year, week):
    for weekdays in WEEKDAYS:

        if weekdays == "saturday" or weekdays == "sunday":
            start = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 00:00", "%Y-%W-%w %H:%M")
            end = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 23:59", "%Y-%W-%w %H:%M")

            weekend_times = dict({"start": start, "end": end})

            create_availablitiy_entry(weekend_times, doctor_id)

        else:
            start_morning = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 00:00", "%Y-%W-%w %H:%M")
            end_morning = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 07:59", "%Y-%W-%w %H:%M")

            morning = dict({"start": start_morning, "end": end_morning})

            create_availablitiy_entry(morning, doctor_id)

            start_break = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 12:31", "%Y-%W-%w %H:%M")
            end_break = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 13:29", "%Y-%W-%w %H:%M")

            break_time = dict({"start": start_break, "end": end_break})

            create_availablitiy_entry(break_time, doctor_id)

            start_evening = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 17:31", "%Y-%W-%w %H:%M")
            end_evening = datetime.strptime(
                f"{year}-{week}-{WEEKDAYS[weekdays]} 23:59", "%Y-%W-%w %H:%M")

            evening = dict({"start": start_evening, "end": end_evening})

            create_availablitiy_entry(evening, doctor_id)

@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    """
    Rendering scheduling page for creating the weekly availabilities for doctors
    :return: render_template with schedule.html
    """
    form = ScheduleBookingForm()
    # TODO Find a way to store globally
    doctors = get_user("doctor")
    doctors_id_name = doctors[0]  # contains tuples of doctor id and names

    # passing the tuples for doctor over to forms for access on View
    form.doctor_id.choices = doctors_id_name

    if form.validate_on_submit():
        # retrieve the selected doctor and patient id from forms
        chosen_doctor_id = form.doctor_id.data

        year = form.year.data

        week = form.calendar_week.data

        build_default_busy_times(chosen_doctor_id, year, week)

        if form.monday_morning.data:
            monday_morning_times = get_work_time("morning", year, week, 'monday')
            create_availablitiy_entry(monday_morning_times, chosen_doctor_id)

        if form.monday_afternoon.data:
            monday_afternoon_times = get_work_time("afternoon", year, week, 'monday')
            create_availablitiy_entry(monday_afternoon_times, chosen_doctor_id)

        if form.tuesday_morning.data:
            tuesday_morning_times = get_work_time("morning", year, week, 'tuesday')
            create_availablitiy_entry(tuesday_morning_times, chosen_doctor_id)

        if form.tuesday_afternoon.data:
            tuesday_afternoon_times = get_work_time("afternoon", year, week, 'tuesday')
            create_availablitiy_entry(tuesday_afternoon_times, chosen_doctor_id)

        if form.wednesday_morning.data:
            wednesday_morning_times = get_work_time("morning", year, week, 'wednesday')
            create_availablitiy_entry(wednesday_morning_times, chosen_doctor_id)

        if form.wednesday_afternoon.data:
            wednesday_afternoon_times = get_work_time("afternoon", year, week, 'wednesday')
            create_availablitiy_entry(wednesday_afternoon_times, chosen_doctor_id)

        if form.thursday_morning.data:
            thursday_morning_times = get_work_time("morning", year, week, 'thursday')
            create_availablitiy_entry(thursday_morning_times, chosen_doctor_id)

        if form.thursday_afternoon.data:
            thursday_afternoon_times = get_work_time("afternoon", year, week, 'thursday')
            create_availablitiy_entry(thursday_afternoon_times, chosen_doctor_id)

        if form.friday_morning.data:
            friday_morning_times = get_work_time("morning", year, week, 'friday')
            create_availablitiy_entry(friday_morning_times, chosen_doctor_id)

        if form.friday_afternoon.data:
            friday_afternoon_times = get_work_time("afternoon", year, week, 'friday')
            create_availablitiy_entry(friday_afternoon_times, chosen_doctor_id)

        # schedule_dict = {"doctor_id": form.doctor_id.data}

    return render_template('schedule.html', title='Schedule', form=form)


def create_availablitiy_entry(date_range, doctor_id):
    google_calendar = gc_api()
    # Post data to Google Calendar API for event creation
    title = f"non-availability time"
    # date = concat_date_time(form.date.data, form.start.data)

    start = format_datetime_str(date_range["start"])
    end = format_datetime_str(date_range["end"])

    google_calendar.book_doctor_times(start=start, end=end, title=title, doctor_id=doctor_id)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Rendering patient registration page and post data to database API
    :return: render_template containing schedule.html and form data
    """
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

                url = f"{API_URL}patients"

                # post the patient registration to DateBase API
                api_response = requests.post(url=url, json=patient_dict)

                if api_response.status_code == 200:
                    flash('Your registration was sucessful', 'success')
                    return redirect(url_for('booking'))
                else:
                    response = json.loads(api_response.text)
                    reason = response["message"]
                    flash(
                        f'Your registration failed. {reason}. Please try again!', 'danger')
                    app.logger.error(f"failed registration{reason}")
                return redirect(url_for('register'))
        return render_template('patient_register.html', title='Register', form=form)
    except Exception as err:
        app.logger.error(err)
        return render_template('500.html'), 500


@app.route("/consultation_list", methods=['GET', 'POST'])
def consultation_list():
    """ Route to a list of consultations which display the patients previous medical history and shall allow
    for creating new consultations notes on basis of bookings
    :return: render_template containing consultation_list.html booking and doctors_id chosen by user
    """
    form = ConsultationForm()

    # TODO Find a way to store globally
    doctors = get_user("doctor")
    doctors_id_name = doctors[0]  # contains tuples of doctor id and names
    form.doctor_id.choices = doctors_id_name

    chosen_doctor_id = form.doctor_id.data

    if chosen_doctor_id is None:
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
            booking_date, config.FORMAT_JSON_DATE_STRING)
        # Adding an end time for it
        booking['appointment_end'] = booking['appointment'] + \
                                     timedelta(minutes=config.CONSULTATION_DURATION)

    return render_template('consultation_list.html', title='Consultation Bookings List', form=form,
                           bookings=bookings, doctors_name=dict(doctors_id_name))


@app.route("/consultation/<consultation_id>", methods=['GET', 'POST', 'PUT'])
def consultation(consultation_id):
    # TODO Test if this works
    """
    Rendering patient consultation note form for the doctor to fill and post to database API
    :return: render_template containing consultation_details.html and form data
    """
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

def booking():
    """
    Rendering booking form and post to database API and to google calender method
    for both creation in google calendar and in database
    :return: render_template containing booking_create.html and form data
    """

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
        form.reason.choices = CHOICES_REASON

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
                                                                            duration=config.CONSULTATION_DURATION)

                    # Building Message Body for database post request
                    consultation = {
                        "appointment": format_datetime_str(concat_date_time(form.date.data, form.start.data)),
                        "patient_id": chosen_patient_id,
                        "doctor_id": chosen_doctor_id,
                        "duration": str(config.CONSULTATION_DURATION),
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
                        return redirect(url_for('calendar', doctor_id=chosen_doctor_id))
                    else:
                        flash(f'Appointment with google event no. {google_event_id} with was successfully created!',
                              'success')
                elif form.delete.data is True:
                    flash(f'Appointment', 'success')
            return redirect(url_for('booking'))
        return render_template('booking_create.html', title='Consultation Booking', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)

@app.route("/calendar_all/")
def calendar_all():
    """
    Route for rendering embedded google calender iframe for clerk user - containing all appointments
    :return: render_template containing calendar.html and doctor_id set to 0
    """
    # TODO needs overwork to post the correct calendar API
    doctor_id = 0

    # Getting the google Calendar ID which is attached to doctor
    # doctor = requests.get(f"{API_URL}doctors/{doctor_id}")
    # doctor = json.loads(doctor.text)
    # google_calendar_id = dict(doctor)["calendar_id"]
    # google_calendar_id = 'cvrsdsk7jjae29p9fg9t6vcr94%40group.calendar.google.com'

    # src=f"https://calendar.google.com/calendar/embed?showTitle=0&amp;showDate=0&amp;showPrint=0&amp;showTabs=0&amp;showCalendars=0&amp;showTz=0&amp;mode=WEEK&amp;height=600&amp;wkst=1&amp;hl=en&amp;bgcolor=%23FFFFFF&amp;src={google_calendar_id}&amp;color=%23B1365F&amp;ctz=Australia%2FMelbourne"
    # iframe = f'<iframe src="{src}" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>'

    return render_template('calendar.html', title='calendar', doctor_id=doctor_id)


@app.route("/calendar/<int:doctor_id>")
def calendar(doctor_id):
    """
    Route for rendering embedded google calender iframe for doctor users only showing the calendar of the doctors calendars
    :param doctor_id: should be declared in http route
    :return: render_template containing calendar.html and doctor_id
    """
    # TODO needs overwork to post the correct calendar API

    # doctor = read_text_file(PATH_DOCTOR)

    return render_template('calendar.html', title='calendar', doctor_id=doctor_id)


@app.route("/statistics")
def statistics():
    """
    Posting and rendering embedded google data studio statistics from datastudio
    :return: render_template with statistics.html
    """

    return render_template('statistics.html', title='statistics')


@app.route("/consultation_booking/<int:booking_id>")
def consultation_booking(booking_id):
    """show to singular booking content for clerk to overview or to cancel if necessary"""

    booking = requests.get(f"{API_URL}consultations/{booking_id}")
    consultation_booking = json.loads(booking.text)

    # Bringing json string of date to datetime
    consultation_booking['appointment'] = datetime.strptime(consultation_booking['appointment'],
                                                            config.FORMAT_JSON_DATE_STRING)
    # Adding an end time for it
    consultation_end = consultation_booking['appointment'] + \
                       timedelta(minutes=config.CONSULTATION_DURATION)

    # TODO Find a way to store globally
    doctors = get_user("doctor")
    doctors_id_name = doctors[0]

    # TODO Find a way to store globally
    patients = get_user("patient")
    patients_id_name = patients[0]

    # TODO Better way to show date time
    return render_template('booking_show.html', title='Consultation Booking', booking=consultation_booking,
                           cause=dict(CHOICES_REASON),
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
            f"{API_URL}consultations/doctors/{chosen_doctor_id }")

    bookings = json.loads(consultation_bookings.text)

    # Bringing json string of date to datetime
    for booking in bookings:
        booking_date = booking['appointment']
        booking['appointment'] = datetime.strptime(
            booking_date, config.FORMAT_JSON_DATE_STRING)
        # Adding an end time for it
        booking['appointment_end'] = booking['appointment'] + \
                                     timedelta(minutes=config.CONSULTATION_DURATION)

    # TODO Find a way to store globally
    patients = get_user("patient")
    patients_id_name = patients[0]

    # TODO Better way to show date time
    return render_template('booking_list.html', title='Consultation Bookings List', form=form,
                           bookings=bookings, doctors_name=dict(doctors_id_name), patients_name=dict(patients_id_name),
                           cause=dict(CHOICES_REASON), doctor_id=chosen_doctor_id)


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
