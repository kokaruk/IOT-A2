from MAPS import db, ma


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64))
    specialization = db.Column(db.String(120), nullable=True)
    calendar_id = db.Column(db.String(120), nullable=True)
    consultations = db.relationship("Consultation", lazy='dynamic')

    def __init__(self, first_name, second_name, last_name, specialization, calendar_id, consultations):
        self.first_name = first_name
        self.second_name = second_name
        self.last_name = last_name
        self.specialization = specialization
        self.calendar_id = calendar_id
        self.consultations = consultations


class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'second_name', 'last_name',
                  'specialization', 'calendar_id', 'consultations')


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
    medicareNumber = db.Column(db.Integer)
    previousDoctor = db.Column(db.String(120), nullable=True)
    previousClinic = db.Column(db.String(120), nullable=True)
    conditions = db.relationship("Condition", lazy='dynamic')
    medications = db.relationship("Medication", lazy='dynamic')
    consultations = db.relationship("Consultation", lazy='dynamic')

    def __init__(self, first_name, second_name, last_name, dob, gender, address, email, phone, medicareNumber, previousDoctor, previousClinic):
        self.first_name = first_name
        self.second_name = second_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.email = email
        self.phone = phone
        self.medicareNumber = medicareNumber
        self.previousDoctor = previousDoctor
        self.previousClinic = previousClinic


class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'second_name', 'last_name', 'dob', 'gender', 'address',
                  'email', 'phone', 'medicareNumber', 'previousDoctor', 'previousClinic')


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    condition = db.Column(db.String(120), nullable=True)

    def __init__(self, patientId, condition):
        self.patientId = patientId
        self.condition = condition


class ConditionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patientId', 'condition')


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    medication = db.Column(db.String(120), nullable=True)

    def __init__(self, patientId, medication):
        self.patientId = patientId
        self.medication = medication


class MedicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patientId', 'medication')


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment = db.Column(db.DateTime)
    patientId = db.Column(db.Integer, db.ForeignKey(
        'patient.id'), nullable=False)
    doctorId = db.Column(db.Integer, db.ForeignKey(
        'doctor.id'), nullable=False)
    duration = db.Column(db.Integer)
    cause = db.Column(db.String(200), nullable=True)
    cancelled = db.Column(db.Boolean, default=False)
    consultationDetails = db.relationship("ConsultationDetails")

    def __init__(self, appointment, patientId, doctorId, duration, cause, cancelled, consultationDetails):
        self.appointment = appointment
        self.patientId = patientId
        self.doctorId = doctorId
        self.duration = duration
        self.cause = cause
        self.cancelled = cancelled
        self.consultationDetails = consultationDetails


class ConsultationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'appointment', 'patientId', 'doctorId',
                  'duration', 'cause', 'cancelled', 'consultationDetails')


class ConsultationDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultationId = db.Column(db.Integer, db.ForeignKey(
        'consultation.id'), nullable=False)
    description = db.Column(db.String(300))
    additionalNotes = db.Column(db.String(300), nullable=True)
    symptoms = db.Column(db.String(120), nullable=True)
    diagnosis = db.Column(db.String(120), nullable=True)
    actualStart = db.Column(db.DateTime, nullable=True)
    actualEnd = db.Column(db.DateTime, nullable=True)

    def __init__(self, consultationId, description, additionalNotes, symptoms, diagnosis, actualStart, actualEnd):
        self.consultationId = consultationId
        self.description = description
        self.additionalNotes = additionalNotes
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.actualStart = actualStart
        self.actualEnd = actualEnd


class ConsultationDetailsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'consultationId', 'description', 'additionalNotes',
                  'symptoms', 'diagnosis', 'actualStart', 'actualEnd')
