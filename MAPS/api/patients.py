from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from MAPS.api import bp
from models import Patient, PatientSchema

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

# Get all patients


@bp.route('/patients', methods=['GET'])
def get_patients():
    all_patients = Patient.query.all()
    result = patients_schema.dump(all_patients)
    return jsonify(result.data)


# Get all patients for a doctor
# Reason for route order: https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/
@bp.route('/doctors/patients/<int:id>', methods=['GET'])
def get_patients_for_doctor(id):
    pass


# Get a patient by id
@bp.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    pass


# Create a patient by id
@bp.route('/patients/<int:id>', methods=['POST'])
def create_patient(id):
    pass


# Update a patient  by id
@bp.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    pass
