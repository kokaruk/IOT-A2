from flask import request, jsonify

from MAPS import db
from MAPS.api import bp
from MAPS.models import Doctor, DoctorSchema

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)


# Get all doctors
@bp.route('/doctors', methods=['GET'])
def get_doctors():
    all_doctors = Doctor.query.all()
    result = doctors_schema.dump(all_doctors)
    return jsonify(result.data)


# Get a doctor by id
@bp.route('/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)
    result = doctor_schema.dump(doctor)
    return jsonify(result.data)


# Get a doctor by email
@bp.route('/doctors/email/<string:email>', methods=['GET'])
def get_doctor_by_email(email):
    doctor = Doctor.query.filter(Doctor.email == email).first()
    result = doctor_schema.dump(doctor)
    return jsonify(result.data)


# Create a doctor
@bp.route('/doctors', methods=['POST'])
def create_doctor():
    first_name = request.json['first_name']
    second_name = request.json['second_name']
    last_name = request.json['last_name']
    email = request.json['email']
    specialization = request.json['specialization']
    calendar_id = request.json['calendar_id']

    new_doctor = Doctor(first_name, second_name, last_name, email, calendar_id, specialization)
    db.session.add(new_doctor)
    db.session.commit()
    return doctor_schema.jsonify(new_doctor)


# Delete a doctor by id
@bp.route('/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    db.session.delete(doctor)
    db.session.commit()
    return doctor_schema.jsonify(doctor)


# Update a doctor's calendar_id by id
@bp.route('/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    doctor.calendar_id = request.json['calendar_id']
    db.session.commit()
    return doctor_schema.jsonify(doctor)
