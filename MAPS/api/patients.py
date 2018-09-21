from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from MAPS.api import bp
from MAPS.api.errors import bad_request
from MAPS import db
from MAPS.models import Patient, Medication, Condition, PatientSchema, MedicationSchema, ConditionSchema

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)
medication_schema = MedicationSchema()
medications_schema = MedicationSchema(many=True)
condition_schema = ConditionSchema()
conditions_schema = ConditionSchema(many=True)


# PATIENTS

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
    medicare_number = request.json['medicare_number']
    previous_doctor = request.json['previous_doctor']
    previous_clinic = request.json['previous_clinic']

    new_patient = Patient(first_name, second_name, last_name, dob, gender,
                          address, email, phone, medicare_number, previous_doctor, previous_clinic)
    db.session.add(new_patient)
    db.session.commit()
    return patient_schema.jsonify(new_patient)


# endpoint to delete patient by id
@bp.route("/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return patient_schema.jsonify(patient)


# MEDICATIONS

# Add a medication for a patient
@bp.route("/patients/<int:id>/medications", methods=["POST"])
def add_medication_to_patient(id):
    patient_id = id
    medication = request.json['medication']
    new_medication = Medication(patient_id, medication)
    db.session.add(new_medication)
    db.session.commit()
    return medication_schema.jsonify(new_medication)


# Get all medications for patient by id
@bp.route("/patients/<int:id>/medications", methods=["GET"])
def get_all_medication_for_patient(id):
    all_medications_for_patient = Medication.query.filter(Medication.patient_id == id).all()
    result = medications_schema.dump(all_medications_for_patient)
    return jsonify(result.data)


# endpoint to delete patient by id
@bp.route("/patients/<int:id>/medications/<int:medication_id>", methods=["DELETE"])
def delete_medication(id, medication_id):
    deleted_medication = Medication.query.filter(Medication.id == medication_id).filter(
        Medication.patient_id == id).first()
    db.session.delete(deleted_medication)
    db.session.commit()
    all_medications_for_patient = Medication.query.filter(Medication.patient_id == id).all()
    result = medications_schema.dump(all_medications_for_patient)
    return jsonify(result.data)


# CONDITIONS

# Add a condition for a patient
@bp.route("/patients/<int:id>/conditions", methods=["POST"])
def add_condition_to_patient(id):
    patient_id = id
    condition = request.json['condition']
    new_condition = Condition(patient_id, condition)
    db.session.add(new_condition)
    db.session.commit()
    return condition_schema.jsonify(new_condition)


# Get all conditions for patient by id
@bp.route("/patients/<int:id>/conditions", methods=["GET"])
def get_all_condition_for_patient(id):
    all_conditions_for_patient = Condition.query.filter(Condition.patient_id == id).all()
    result = conditions_schema.dump(all_conditions_for_patient)
    return jsonify(result.data)


# Delete a condition for a patient by patient id
@bp.route("/patients/<int:id>/conditions/<int:condition_id>", methods=["DELETE"])
def delete_condition(id, condition_id):
    deleted_condition = Condition.query.filter(Condition.id == condition_id).filter(Condition.patient_id == id).first()
    db.session.delete(deleted_condition)
    db.session.commit()
    all_conditions_for_patient = Condition.query.filter(Condition.patient_id == id).all()
    result = conditions_schema.dump(all_conditions_for_patient)
    return jsonify(result.data)
