from flask import render_template, url_for, flash, redirect, request, jsonify
from MAPS.forms import RegistrationForm, ConsultationForm, BookingForm
from MAPS import app
from MAPS.utils import concat_date_time, write_text_file, read_text_file
from MAPS.calendar_entry import Google_Calendar_API as gc_api

CONSULTATION_DURATION = 20
PATH_DOCTOR = "MAPS/credentials/doctor.txt"


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
    # TODO get POST Method to POST to API
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                # jsonified/serialized version
                patient_jsonified = jsonify(first_name=form.firstname.data,
                                            second_name=form.secondname.data,
                                            last_name=form.lastname.data,
                                            dob=form.dob.data,
                                            gender=form.gender.data,
                                            address=form.address.data,
                                            email=form.email.data,
                                            phone=form.phone.data,
                                            medicareNumber=form.medicare.data,
                                            previousDoctor=form.pre_doctor.data,
                                            previousClinic=form.pre_clinic.data
                                            )
                # dictionary version
                patient_dict = {"first_name": form.firstname.data,
                                "second_name": form.secondname.data,
                                "last_name": form.lastname.data,
                                "dob": form.dob.data,
                                "gender": form.gender.data,
                                "address": form.address.data,
                                "email": form.email.data,
                                "phone": form.phone.data,
                                "medicareNumber": form.medicare.data,
                                "previousDoctor": form.pre_doctor.data,
                                "previousClinic": form.pre_clinic.data
                                }
                return redirect(url_for('api.create_patient', patient=patient_jsonified))
            flash('Your registration was successful!', 'success')
            return redirect(url_for('home'))
        return render_template('patient_register.html', title='Register', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/consultation", methods=['GET', 'POST'])
def consultation():
    """Rendering patient consultation details page and post to database API """
    # TODO get POST Method to POST to API
    try:
        form = ConsultationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                consulatation_details = jsonify(first_name=form.description.data,
                                                second_name=form.additional_notes.data,
                                                last_name=form.symptoms.data,
                                                dob=form.diagnosis.data,
                                                gender=concat_date_time(form.date.data, form.start.data),
                                                address=concat_date_time(form.date.data, form.end.data),
                                                )
                return redirect(url_for('api.create_consultation', new_consultation_details=consulatation_details))
            flash('Consultation was successfully saved!', 'success')
            return redirect(url_for('home'))
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
        if form.validate_on_submit():
            if request.method == 'POST':
                consultation = jsonify(
                    appointment=concat_date_time(form.date.data, form.start.data),
                    patientId=form.patient_name.data,
                    doctorId=form.doctor_name.data,
                    duration=str(CONSULTATION_DURATION),
                    cause=form.reason.data,
                    cancelled=form.cancelled.data,
                )
                # TODO Comment out once Forms to API work
                # return redirect(url_for('api.create_consultation_details', new_consultation=consultation))
            google_calendar = gc_api()

            index_reason = int(form.reason.data)
            reason = form.reason.choices[index_reason][1]

            index_doctor = int(form.doctor_name.data)
            doctor = form.doctor_name.choices[index_doctor][1]

            # TODO Smarter way to transfer the chosen doctor to the calendar entry creation
            write_text_file(PATH_DOCTOR, doctor)

            title = f"Patient: {form.patient_name.data} Issue : {reason}"
            date = concat_date_time(form.date.data, form.start.data)
            google_calendar.insert_calendar_entry(title=title, date=date, patient_email="fightme1984@gmail.com",
                                                  doctor_email="akbar.dakbar@shojiido.de",
                                                  doctor=doctor, duration=CONSULTATION_DURATION)

            flash('Appointment was successfully created!', 'success')
            return redirect(url_for('calendar'))
        return render_template('booking.html', title='Consultation Booking', form=form)
    except Exception as err:
        # TODO better Exception handling
        print(err)


@app.route("/calendar")
def calendar():
    """Posting google calender API  """
    doctor = read_text_file(PATH_DOCTOR)

    return render_template('calendar.html', title='calendar', doctor=doctor)
