from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from MAPS.api import bp
from MAPS.api.errors import bad_request
from MAPS import db
from MAPS.models import Patient, PatientSchema

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)


# Get all patients
@bp.route('/patients', methods=['GET'])
def get_patients():
    all_patients = Patient.query.all()
    result = patients_schema.dump(all_patients)
    return jsonify(result.data)


# Get a patient by id
@bp.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    result = patient_schema.dump(patient)
    return jsonify(result.data)


# Create a patient
@bp.route('/patients', methods=['POST'])
def create_patient():
    first_name = request.json['first_name']
    second_name = request.json['second_name']
    last_name = request.json['last_name']
    dob = request.json['dob']
    gender = request.json['gender']
    address = request.json['address']
    email = request.json['email']
    phone = request.json['phone']
    medicareNumber = request.json['medicareNumber']
    previousDoctor = request.json['previousDoctor']
    previousClinic = request.json['previousClinic']

    new_patient = Patient(first_name, second_name, last_name, dob, gender,
                          address, email, phone, medicareNumber, previousDoctor, previousClinic)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(patient_schema.dump(new_patient))


# Update a patient  by id
@bp.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    # TODO
    pass


# endpoint to delete patient by id
@bp.route("/patients/<id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return patient_schema.jsonify(patient)
