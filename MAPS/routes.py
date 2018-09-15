from flask import render_template, url_for, flash, redirect
from datetime import datetime
from MAPS.forms import RegistrationForm, ConsultationForm, BookingForm
from MAPS import app
from MAPS.calendar_entry import Google_Calendar_API as gc_api


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
    if form.validate_on_submit():
        flash('Your registration was successful!', 'success')
        return redirect(url_for('home'))
    return render_template('patient_register.html', title='Register', form=form)


@app.route("/consultation", methods=['GET', 'POST'])
def consultation():
    form = ConsultationForm()
    if form.validate_on_submit():
        flash('Consultation was successfully saved!', 'success')
        return redirect(url_for('home'))
    return render_template('consultation.html', title='Consultation', form=form)


@app.route("/booking", methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        google_calendar = gc_api()
        date = datetime.combine(form.date.data, form.start.data)
        index_reason = int(form.reason.data)
        reason = form.reason.choices[index_reason][1]

        index_doctor = int(form.doctor_name.data)
        doctor = form.doctor_name.choices[index_doctor][1]

        w = open("MAPS/credentials/doctor.txt", "w")
        w.write(doctor)

        title = f"Patient: {form.patient_name.data} Issue : {reason}"
        google_calendar.insert_calendar_entry(title=title, date=date, patient_email="fightme1984@gmail.com",
                                              patient=form.patient_name, doctor_email="akbar.dakbar@shojiido.de",
                                              doctor=doctor, duration=20)
        flash('Appointment was successfully created!', 'success')
        return redirect(url_for('calendar'))
    return render_template('booking.html', title='Consultation Booking', form=form)


@app.route("/calendar")
def calendar():
    doctor = open("MAPS/credentials/doctor.txt", "r")
    return render_template('calendar.html', title='calendar', doctor=doctor)
