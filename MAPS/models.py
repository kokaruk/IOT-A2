from MAPS import db, ma


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    specialization = db.Column(db.String(120), nullable=True)
    calendar_id = db.Column(db.String(120), nullable=True)
    consultations = db.relationship("Consultation", lazy='dynamic')

    # todo make optional params for init
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


class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'second_name', 'last_name', 'dob', 'gender', 'address',
                  'email', 'phone', 'medicare_number', 'previous_doctor', 'previous_clinic')


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    condition = db.Column(db.String(120), nullable=True)

    def __init__(self, patient_id, condition):
        self.patient_id = patient_id
        self.condition = condition

    def __repr__(self):
        """ for cli output"""
        return f"<Condition {self.condition}>"


class ConditionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'condition')


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    medication = db.Column(db.String(120), nullable=True)

    def __init__(self, patient_id, medication):
        self.patient_id = patient_id
        self.medication = medication

    def __repr__(self):
        """ for cli output"""
        return f"<Condition {self.condition}>"


class MedicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'medication')


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'doctor.id'), nullable=False)
    duration = db.Column(db.Integer)
    cause = db.Column(db.String(200), nullable=True)
    cancelled = db.Column(db.Boolean, default=False)
    consultation_details = db.relationship("consultation_details")

    def __init__(self, appointment, patient_id, doctor_id, duration, cause, cancelled, consultation_details):
        self.appointment = appointment
        self.patientId = patient_id
        self.doctor_id = doctor_id
        self.duration = duration
        self.cause = cause
        self.cancelled = cancelled
        self.consultation_details = consultation_details

    def __repr__(self):
        """ for cli output"""
        return f"<Consultation {self.appointment}>"


class ConsultationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'appointment', 'patient_id', 'doctor_id',
                  'duration', 'cause', 'cancelled', 'consultation_details')


class ConsultationDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultationId = db.Column(db.Integer, db.ForeignKey(
        'consultation.id'), nullable=False)
    description = db.Column(db.String(300))
    additional_notes = db.Column(db.String(300), nullable=True)
    symptoms = db.Column(db.String(120), nullable=True)
    diagnosis = db.Column(db.String(120), nullable=True)
    actual_start = db.Column(db.DateTime, nullable=True)
    actual_end = db.Column(db.DateTime, nullable=True)

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


class ConsultationDetailsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'consultation_id', 'description', 'additional_notes',
                  'symptoms', 'diagnosis', 'actual_start', 'actual_end')
