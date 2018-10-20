from flask import render_template, url_for, redirect, request, flash

from app import app
from app.greeter_client import notify
from forms import RegistrationForm
from config import Config


@app.route("/")
def index():
    return render_template("home.html", title="Sign in")


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    form = RegistrationForm()
    if form.validate_on_submit():
        greeting = f"Patient {form.firstname.data} {form.lastname.data} arrived for consultation"
        notify(Config.GRPC_MASTER_IP, greeting)
        return redirect('/')
    return render_template('checkin.html', title='Sign In', form=form)
