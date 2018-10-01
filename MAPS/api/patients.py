from flask import request, jsonify

from MAPS.api import bp
from MAPS.api.errors import bad_request
from MAPS import db
from MAPS.models import Patient, Medication, Condition, MedicalCertificate, Referral
from MAPS.models import PartPatientSchema, FullPatientSchema, MedicationSchema, ConditionSchema, \
    MedicalCertificateSchema, ReferralSchema

part_patient_schema = PartPatientSchema()
part_patients_schema = PartPatientSchema(many=True)

full_patient_schema = FullPatientSchema()
full_patients_schema = FullPatientSchema(many=True)

medication_schema = MedicationSchema()
medications_schema = MedicationSchema(many=True)

condition_schema = ConditionSchema()
conditions_schema = ConditionSchema(many=True)

medical_certificate_schema = MedicalCertificateSchema()
medical_certificates_schema = MedicalCertificateSchema(many=True)

referral_schema = ReferralSchema()
referrals_schema = ReferralSchema(many=True)


# PATIENTS

# Get all patients
@bp.route('/patients', methods=['GET'])
def get_patients():
    """
        This route returns all patients in the database
    :return: JSON array of patients
    """
    all_patients = Patient.query.all()
    result = part_patients_schema.dump(all_patients)
    return jsonify(result.data)


#  a patient by id
@bp.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    """
        This route returns a single patient matching the id provided. Does not include related data.
    :param patient id:
    :return: Patient as a JSON object.
    """
    patient = Patient.query.get(id)
    result = part_patient_schema.dump(patient)
    return jsonify(result.data)


# Get a patient by id - include all related data
@bp.route('/patients/<int:id>/all', methods=['GET'])
def get_patient_include_related_data(id):
    """
        This route returns a single patient matching the id provided. Includes related data.
    :param patient id:
    :return: Patient as a JSON object, with related data.
    """
    patient = Patient.query.get(id)
    result = full_patient_schema.dump(patient)
    return jsonify(result.data)


# Create a patient
@bp.route('/patients', methods=['POST'])
def create_patient():
    """
        This route accepts a Patient JSON object, and adds to the database.
    :return: Patient as a JSON object.
    """
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
    return part_patient_schema.jsonify(new_patient)


# endpoint to delete patient by id
@bp.route("/patients", methods=["DELETE"])
def delete_patient():
    """
        This route accepts a json object of the patient's id to delete.
    :return: Deleted Patient as a JSON object.
    """
    id = request.json['id']
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return part_patient_schema.jsonify(patient)


# MEDICATIONS

# Add a medication for a patient
@bp.route("/patients/<int:patient_id>/medications", methods=["POST"])
def add_medication_to_patient(patient_id):
    """
        This route accepts a patient id and medication JSON object from request
        to create a medication for a patient.
    :param patient_id:
    :return: Medication JSON object.
    """
    medication = request.json['medication']
    consultation_details_id = request.json['consultation_details_id']
    new_medication = Medication(patient_id, medication, consultation_details_id)
    db.session.add(new_medication)
    db.session.commit()
    return medication_schema.jsonify(new_medication)


# Get all medications for patient by id
@bp.route("/patients/<int:patient_id>/medications", methods=["GET"])
def get_all_medication_for_patient(patient_id):
    """
        This route accepts a patient id and returns all the patient's medications.
    :param patient_id:
    :return: JSON array of patient's medications.
    """
    all_medications_for_patient = Medication.query.filter(Medication.patient_id == patient_id).all()
    result = medications_schema.dump(all_medications_for_patient)
    return jsonify(result.data)


# endpoint to delete patient by id
@bp.route("/patients/<int:patient_id>/medications", methods=["DELETE"])
def delete_medication(patient_id):
    """
    This route takes a patient id parameter, and a medication id as a JSON object from the request to delete a
    medication for a patient.
    :param patient_id:
    :return: JSON array of all the patient's medications.
    """
    id = request.json['id']
    deleted_medication = Medication.query.filter(Medication.id == id).filter(
        Medication.patient_id == patient_id).first()
    db.session.delete(deleted_medication)
    db.session.commit()
    all_medications_for_patient = Medication.query.filter(Medication.patient_id == patient_id).all()
    result = medications_schema.dump(all_medications_for_patient)
    return jsonify(result.data)


# CONDITIONS

# Add a condition for a patient
@bp.route("/patients/<int:patient_id>/conditions", methods=["POST"])
def add_condition_to_patient(patient_id):
    """
        This route takes a patient id, and condition JSON object from the request to add a condition for a
        patient.
    :param patient_id:
    :return: Condition JSON object for patient.
    """
    condition = request.json['condition']
    consultation_details_id = request.json['consultation_details_id']
    new_condition = Condition(patient_id, condition, consultation_details_id)
    db.session.add(new_condition)
    db.session.commit()
    return condition_schema.jsonify(new_condition)


# Get all conditions for patient by id
@bp.route("/patients/<int:patient_id>/conditions", methods=["GET"])
def get_all_condition_for_patient(patient_id):
    """
        This route takes a patient id to return all the conditions for a patient.
    :param patient_id:
    :return: JSON array of conditions for a patient.
    """
    all_conditions_for_patient = Condition.query.filter(Condition.patient_id == patient_id).all()
    result = conditions_schema.dump(all_conditions_for_patient)
    return jsonify(result.data)


# Delete a condition for a patient by patient id
@bp.route("/patients/<int:patient_id>/conditions", methods=["DELETE"])
def delete_condition(patient_id):
    """
        This route takes a patient id and condition id from JSON object in request to delete a condition for a
        patient.
    :param patient_id:
    :return: JSON array of all conditions for a patient.
    """
    id = request.json['id']
    deleted_condition = Condition.query.filter(Condition.id == id).filter(Condition.patient_id == patient_id).first()
    db.session.delete(deleted_condition)
    db.session.commit()
    all_conditions_for_patient = Condition.query.filter(Condition.patient_id == patient_id).all()
    result = conditions_schema.dump(all_conditions_for_patient)
    return jsonify(result.data)
