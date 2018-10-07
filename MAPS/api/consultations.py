"""
.. module:: MAPS.api.consultations
    :synopsis: Consultations restful api

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from flask import jsonify, request
from MAPS.api import bp
from MAPS import db
from MAPS.models import Consultation, ConsultationDetails, FullConsultationSchema, ConsultationDetailsSchema

consultation_schema = FullConsultationSchema()
consultations_schema = FullConsultationSchema(many=True)

consultation_detail_schema = ConsultationDetailsSchema()
consultation_details_schema = ConsultationDetailsSchema(many=True)


# Get all consultations for a particular id
@bp.route('/consultations/<int:id>', methods=['GET'])
def get_consultation(id):
    """
    This route returns a single consultation matching the id provided. Includes related data.
    :param consultation id:
    :return: Consultation as a JSON object.
    """
    consultation = Consultation.query.get(id)
    result = consultation_schema.dump(consultation)
    return jsonify(result.data)


# Get all consultations for a particular doctor
@bp.route('/consultations/doctors/<int:id>', methods=['GET'])
def get_consultations_doctor(id):
    """
    This route returns all the consultations for the doctor of the id provided.
    :param doctor id:
    :return: JSON array of consultations.
    """
    all_consultations_for_a_doctor = Consultation.query.filter(
        Consultation.doctor_id == id).all()
    result = consultations_schema.dump(all_consultations_for_a_doctor)
    return jsonify(result.data)


# Get all consultations for a particular patient
@bp.route('/consultations/patients/<int:id>', methods=['GET'])
def get_consultations_patient(id):
    """
    This route returns all the consultations for the patient of the id provided.
    :param patient id:
    :return: JSON array of consultations.
    """
    all_consultations_for_a_patient = Consultation.query.filter(
        Consultation.patient_id == id).all()
    result = consultations_schema.dump(all_consultations_for_a_patient)
    return jsonify(result.data)


# Create a consultation
@bp.route('/consultations', methods=['POST'])
def create_consultation():
    """
    This route accepts a Consultation JSON object, and adds to the database.
    :return: Consultation as a JSON object.
    """
    # get all information from body
    appointment = request.json['appointment']
    patient_id = request.json['patient_id']
    doctor_id = request.json['doctor_id']
    duration = request.json['duration']
    cause = request.json['cause']
    cancelled = request.json['cancelled']
    google_event_id = request.json['google_event_id']

    new_consultation = Consultation(
        appointment, patient_id, doctor_id, duration, cause, cancelled, google_event_id)
    db.session.add(new_consultation)
    db.session.commit()
    consultation_detail = ConsultationDetails(
        new_consultation.id, None, None, None, None, None, None)
    db.session.add(consultation_detail)
    db.session.commit()
    return consultation_schema.jsonify(new_consultation)


# Update a calendar_cancelled status by id
@bp.route('/consultations/<int:id>', methods=['PUT'])
def update_consultation(id):
    """
    This route updates a consultation cancelled status.
    :param Consultation id:
    :return: Consultation as a JSON object.
    """
    consultation = Consultation.query.get(id)
    consultation.cancelled = request.json['cancelled']
    db.session.commit()
    return consultation_schema.jsonify(consultation)


# Get all consultations for a particular doctor
@bp.route('/consultations/details/<int:id>', methods=['GET'])
def get_consultation_detail(id):
    """
    This route returns a the consultation detail for a consultation of the id provided.
    :param consultation id:
    :return: Consultation detail JSON object.
    """
    consultation_detail = ConsultationDetails.query.get(id)
    result = consultation_detail_schema.dump(consultation_detail)
    return jsonify(result.data)


# Create a consultationDetail for a particular consultation
@bp.route('/consultations/details', methods=['POST'])
def create_consultation_detail():
    """
    This route creates a ConsultationDetails, and adds to the database.
    :return: ConsultationDetails JSON object.
    """
    # get updated information from body
    consultation_id = request.json['consultation_id']
    # limit notes to one per consultation
    all_details = ConsultationDetails.query.filter(
        ConsultationDetails.consultation_id == consultation_id).all()
    if len(all_details) > 0:
        return get_consultation_detail(all_details[0].id)

    description = request.json['description']
    additional_notes = request.json['additional_notes']
    symptoms = request.json['symptoms']
    diagnosis = request.json['diagnosis']
    actual_start = request.json['actual_start']
    actual_end = request.json['actual_end']

    consultation_detail = ConsultationDetails(consultation_id, description, additional_notes,
                                              symptoms, diagnosis, actual_start, actual_end)
    db.session.add(consultation_detail)
    db.session.commit()
    return consultation_detail_schema.jsonify(consultation_detail)


@bp.route('/consultations/details/<int:id>', methods=['PUT'])
def edit_consultation_detail(id):
    """
    This route updates a ConsultationDetails. Provide the entire ConsultationDetails in the request body. All fields
    are saved.
    :param ConsultationDetails id:
    :return: ConsultationDetails JSON object.
    """
    # get updated information from body
    consultation_detail = ConsultationDetails.query.get(id)
    description = request.json['description']
    consultation_detail.description = description

    additional_notes = request.json['additional_notes']
    consultation_detail.additional_notes = additional_notes

    symptoms = request.json['symptoms']
    consultation_detail.symptoms = symptoms

    diagnosis = request.json['diagnosis']
    consultation_detail.diagnosis = diagnosis

    actual_start = request.json['actual_start']
    consultation_detail.actual_start = actual_start

    actual_end = request.json['actual_end']
    consultation_detail.actual_end = actual_end

    db.session.commit()
    return consultation_detail_schema.jsonify(consultation_detail)


# Delete a consultationDetail and return the whole consultation
@bp.route('/consultations/details/<int:id>', methods=['DELETE'])
def delete_consultation_detail(id):
    """
    This route deletes a ConsultationDetails.
    :param ConsultationDetails id:
    :return: ConsultationDetails JSON object.
    """
    consultation_detail = ConsultationDetails.query.get(id)
    consultation = Consultation.query.get(consultation_detail.consultation_id)
    db.session.delete(consultation_detail)
    db.session.commit()
    return consultation_schema.jsonify(consultation)
