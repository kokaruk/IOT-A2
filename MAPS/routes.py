from flask import render_template, url_for, flash, redirect, request
from MAPS.forms import RegistrationForm, ConsultationForm, BookingForm
from MAPS import app
from MAPS.utils import concat_date_time, write_text_file, read_text_file
# from MAPS import api_bp
from MAPS.calendar_entry import Google_Calendar_API as gc_api

CONSULTATION_DURATION = 20
PATH_DOCTOR = "MAPS/credentials/doctor.txt"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = request.form['firstname']
        second_name = request.form['secondname']
        last_name = request.form['lastname']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        patient = (first_name, second_name, last_name, dob, gender, address, email, phone)
        flash('Your registration was successful!', 'success')
        return redirect(url_for('home'))
    return render_template('patient_register.html', title='Register', form=form)


@app.route("/consultation", methods=['GET', 'POST'])
def consultation():
    form = ConsultationForm()
    if request.method == 'POST' and form.validate_on_submit():
        description = request.form['description']
        additionalNotes = request.form['additional_notes']
        symptoms = request.form['symptoms']
        diagnosis = request.form['diagnosis']
        actualStart = concat_date_time(form.date.data, form.start.data)
        actualEnd = concat_date_time(form.date.data, form.end.data)
        consulatation_details = (description, additionalNotes, symptoms, diagnosis, actualStart, actualEnd)
        flash('Consultation was successfully saved!', 'success')
        return redirect(url_for('home'))
    return render_template('consultation.html', title='Consultation', form=form)


@app.route("/booking", methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        appointment = concat_date_time(form.date.data, form.start.data)
        patientId = request.form["patient_name"]
        doctorId = request.form["doctor_name"]
        duration = str(CONSULTATION_DURATION)
        cause = request.form["reason"]
        cancelled = request.form["cancelled"]
        consultation = (appointment, patientId, doctorId, duration, cause, cancelled)

        google_calendar = gc_api()

        index_reason = int(form.reason.data)
        reason = form.reason.choices[index_reason][1]

        index_doctor = int(form.doctor_name.data)
        doctor = form.doctor_name.choices[index_doctor][1]

        write_text_file(PATH_DOCTOR, doctor)

        title = f"Patient: {form.patient_name.data} Issue : {reason}"
        google_calendar.insert_calendar_entry(title=title, date=date, patient_email="fightme1984@gmail.com",
                                              patient=form.patient_name, doctor_email="akbar.dakbar@shojiido.de",
                                              doctor=doctor, duration=20)
        flash('Appointment was successfully created!', 'success')
        return redirect(url_for('calendar'))
    return render_template('booking.html', title='Consultation Booking', form=form)


@app.route("/calendar")
def calendar():
    doctor = read_text_file(PATH_DOCTOR)

    return render_template('calendar.html', title='calendar', doctor=doctor)
