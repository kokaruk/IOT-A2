from flask import render_template, url_for, flash, redirect
from MAPS.forms import RegistrationForm, ConsultationForm
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
    return render_template('patient_register.html', title='Register', form=form)


@app.route("/consultation", methods=['GET', 'POST'])
def consultation():
    form = ConsultationForm()
    return render_template('consultation.html', title='Consultation', form=form)
