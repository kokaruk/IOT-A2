from marshmallow import fields

from MAPS import db, ma


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    consultation_details_id = db.Column(db.Integer, db.ForeignKey('consultation_details.id'), nullable=False)
    procedure_name = db.Column(db.String(120))
    referred_practitioner = db.Column(db.String(120))

    def __init__(self, patient_id, consultation_details_id, procedure_name, referred_practitioner):
        self.patient_id = patient_id
        self.consultation_details_id = consultation_details_id
        self.procedure_name = procedure_name
        self.referred_practitioner = referred_practitioner

    def __repr__(self):
        """ for cli output"""
        return f"<procedure_name {self.procedure_name}>"


class ReferralSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'consultation_details_id', 'procedure_name', 'referred_practitioner')


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    consultation_details_id = db.Column(db.Integer, db.ForeignKey('consultation_details.id'), nullable=False)
    medication = db.Column(db.String(120), nullable=True)

    def __init__(self, patient_id, medication, consultation_details_id):
        self.patient_id = patient_id
        self.medication = medication
        self.consultation_details_id = consultation_details_id

    def __repr__(self):
        """ for cli output"""
        return f"<Medication {self.medication}>"


class MedicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'consultation_details_id', 'medication')


class MedicalCertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    consultation_details_id = db.Column(db.Integer, db.ForeignKey('consultation_details.id'), nullable=False)
    certificate = db.Column(db.String(120), nullable=True)

    def __init__(self, patient_id, consultation_details_id, certificate):
        self.patient_id = patient_id
        self.consultation_details_id = consultation_details_id
        self.certificate = certificate

    def __repr__(self):
        """ for cli output"""
        return f"<certificate {self.certificate}>"


class MedicalCertificateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'consultation_details_id', 'certificate')


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    consultation_details_id = db.Column(db.Integer, db.ForeignKey('consultation_details.id'), nullable=False)
    condition = db.Column(db.String(120), nullable=True)

    def __init__(self, patient_id, condition, consultation_details_id):
        self.patient_id = patient_id
        self.consultation_details_id = consultation_details_id
        self.condition = condition

    def __repr__(self):
        """ for cli output"""
        return f"<Condition {self.condition}>"


class ConditionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'consultation_details_id', 'condition')


class ConsultationDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=False)
    description = db.Column(db.String(300))
    additional_notes = db.Column(db.String(300), nullable=True)
    symptoms = db.Column(db.String(120), nullable=True)
    diagnosis = db.Column(db.String(120), nullable=True)
    actual_start = db.Column(db.DateTime, nullable=True)
    actual_end = db.Column(db.DateTime, nullable=True)
    medication_id = db.relationship("Medication")
    condition = db.relationship("Condition")
    referral = db.relationship("Referral")
    medical_certificate = db.relationship("MedicalCertificate")

    def __init__(self, consultation_id, description, additional_notes, symptoms, diagnosis, actual_start, actual_end):
        self.consultation_id = consultation_id
        self.description = description
        self.additional_notes = additional_notes
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.actual_start = actual_start
        self.actual_end = actual_end

    def __repr__(self):
        """ for cli output"""
        return f"<ConsultationDetails {self.description}>"


# class ConsultationDetailsSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'consultation_id', 'description', 'additional_notes',
#                   'symptoms', 'diagnosis', 'actual_start', 'actual_end')
class ConsultationDetailsSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    consultation_id = fields.Int(dump_only=True)
    description = fields.Str(dump_only=True)
    additional_notes = fields.Str(dump_only=True)
    symptoms = fields.Str(dump_only=True)
    diagnosis = fields.Str(dump_only=True)
    actual_start = fields.DateTime(dump_only=True)
    actual_end = fields.DateTime(dump_only=True)
    condition = fields.Nested(ConditionSchema, many=True)
    referral = fields.Nested(ReferralSchema, many=True)
    medical_certificate = fields.Nested(MedicalCertificateSchema, many=True)


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    duration = db.Column(db.Integer)
    cause = db.Column(db.String(200), nullable=True)
    cancelled = db.Column(db.Boolean, default=False)
    google_event_id = db.Column(db.String(120), nullable=False)
    consultation_details = db.relationship("ConsultationDetails")

    def __init__(self, appointment, patient_id, doctor_id, duration, cause, cancelled, google_event_id):
        self.appointment = appointment
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.duration = duration
        self.cause = cause
        self.cancelled = cancelled
        self.google_event_id = google_event_id

    def __repr__(self):
        """ for cli output"""
        return f"<Consultation {self.appointment}>"


class ConsultationSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    appointment = fields.DateTime(dump_only=True)
    patient_id = fields.Int(dump_only=True)
    doctor_id = fields.Int(dump_only=True)
    duration = fields.Int(dump_only=True)
    cause = fields.Str(dump_only=True)
    cancelled = fields.Bool(dump_only=True)
    google_event_id = fields.Str(dump_only=True)


class FullConsultationSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    appointment = fields.DateTime(dump_only=True)
    patient_id = fields.Int(dump_only=True)
    doctor_id = fields.Int(dump_only=True)
    duration = fields.Int(dump_only=True)
    cause = fields.Str(dump_only=True)
    cancelled = fields.Bool(dump_only=True)
    google_event_id = fields.Str(dump_only=True)
    consultation_details = fields.Nested(ConsultationDetailsSchema, many=True)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    specialization = db.Column(db.String(120), nullable=True)
    calendar_id = db.Column(db.String(120), nullable=True)
    consultations = db.relationship("Consultation", lazy='dynamic')

    def __init__(self, first_name, second_name, last_name, email, calendar_id, specialization="GP"):
        self.first_name = first_name
        self.second_name = second_name
        self.last_name = last_name
        self.email = email
        self.specialization = specialization
        self.calendar_id = calendar_id

    def __repr__(self):
        """for cli output"""
        return f"<Doctor {self.first_name}>"


class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'second_name', 'last_name',
                  'email', 'calendar_id', 'specialization')


class FullDoctorSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    second_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    specialization = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    calendar_id = fields.Int(dump_only=True)
    consultations = fields.Nested(ConsultationSchema, many=True)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(12))
    address = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(12))
    medicare_number = db.Column(db.Integer)
    previous_doctor = db.Column(db.String(120), nullable=True)
    previous_clinic = db.Column(db.String(120), nullable=True)
    conditions = db.relationship("Condition", lazy='dynamic')
    medications = db.relationship("Medication", lazy='dynamic')
    consultations = db.relationship("Consultation", lazy='dynamic')
    referrals = db.relationship("Referral", lazy='dynamic')

    def __init__(self, first_name, second_name, last_name, dob, gender, address, email, phone, medicare_number,
                 previous_doctor, previous_clinic):
        self.first_name = first_name
        self.second_name = second_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.email = email
        self.phone = phone
        self.medicare_number = medicare_number
        self.previous_doctor = previous_doctor
        self.previous_clinic = previous_clinic

    def __repr__(self):
        """ for cli output"""
        return f"<Patient {self.first_name}>"


class FullPatientSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    second_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    dob = fields.DateTime(dump_only=True)
    gender = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    phone = fields.Str(dump_only=True)
    medications = fields.Nested(MedicationSchema, many=True)
    conditions = fields.Nested(ConditionSchema, many=True)
    consultations = fields.Nested(ConsultationSchema, many=True)
    referrals = fields.Nested(ReferralSchema, many=True)


class PartPatientSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    second_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    dob = fields.DateTime(dump_only=True)
    gender = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    phone = fields.Str(dump_only=True)
