from flask import jsonify, request
from MAPS.api import bp
from MAPS.api.errors import bad_request
from MAPS import db
from MAPS.models import Consultation, ConsultationDetails, ConsultationSchema, FullConsultationSchema, \
    ConsultationDetailsSchema

consultation_schema = FullConsultationSchema()
consultations_schema = ConsultationSchema(many=True)

consultation_detail_schema = ConsultationDetailsSchema()
consultation_details_schema = ConsultationDetailsSchema(many=True)


# Get all consultations for a particular id
@bp.route('/consultations/<int:id>', methods=['GET'])
def get_consultation(id):
    consultation = Consultation.query.get(id)
    result = consultation_schema.dump(consultation)
    return jsonify(result.data)


# Get all consultations for a particular doctor
@bp.route('/consultations/doctors/<int:id>', methods=['GET'])
def get_consultations_doctor(id):
    all_consultations_for_a_doctor = Consultation.query.filter(Consultation.doctor_id == id).all()
    result = consultations_schema.dump(all_consultations_for_a_doctor)
    return jsonify(result.data)


# Get all consultations for a particular patient
@bp.route('/consultations/patients/<int:id>', methods=['GET'])
def get_consultations_patient(id):
    all_consultations_for_a_patient = Consultation.query.filter(Consultation.patient_id == id).all()
    result = consultations_schema.dump(all_consultations_for_a_patient)
    return jsonify(result.data)


# Create a consultation
@bp.route('/consultations', methods=['POST'])
def create_consultation():
    # get all information from body
    appointment = request.json['appointment']
    patient_id = request.json['patient_id']
    doctor_id = request.json['doctor_id']
    duration = request.json['duration']
    cause = request.json['cause']
    cancelled = request.json['cancelled']
    google_event_id = request.json['google_event_id']

    new_consultation = Consultation(appointment, patient_id, doctor_id, duration, cause, cancelled, google_event_id)
    db.session.add(new_consultation)
    db.session.commit()
    return consultations_schema.jsonify(new_consultation)


# Update a calendar_cancelled status by id
@bp.route('/consultations/<int:id>', methods=['PUT'])
def update_consultation(id):
    consultation = Consultation.query.get(id)
    consultation.cancelled = request.json['cancelled']
    db.session.commit()
    return consultations_schema.jsonify(consultation)


# Delete a consultation by id
@bp.route('/consultations/<int:id>', methods=['DELETE'])
def delete_consultation(id):
    pass


# Create a consultationDetail for a particular consultation
@bp.route('/consultations/details/<int:id>', methods=['POST'])
def create_consultation_detail(id):
    # get updated information from body
    consultation_id = request.json['consultation_id']
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


# Delete a consultationDetail
@bp.route('/consultations/details/<int:id>', methods=['DELETE'])
def delete_consultation_detail(id):
    pass
