from flask import render_template, url_for, flash, redirect
from MAPS.forms import RegistrationForm, ConsultationForm, BookingForm
from MAPS import app


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
        flash('Appointment was successfully created!', 'success')
        return redirect(url_for('home'))
    return render_template('booking.html', title='Consultation Booking', form=form)
