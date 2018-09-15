from app import db, ma


class Person(db.Model, ma.Schema):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(12))
    address = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(12))
    _mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }


class Doctor(Person):
    doctorId = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, foreign_keys=Person.id, primary_key=True)
    specialization = db.Column()


class Patient(Person):
    patientId = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, foreign_keys=Person.id, primary_key=True)
    medicareNumber = db.Column(db.Integer)
    previousDoctor = db.Column(db.String(120), nullable=True)
    previousClinic = db.Column(db.String(120), nullable=True)


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, foreign_keys=Patient.patientId)
    condition = db.Column(db.String(120), nullable=True)


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, foreign_keys=Patient.patientId)
    medication = db.Column(db.String(120), nullable=True)


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment = db.Column(db.DateTime)
    patientId = db.Column(db.Integer, foreign_keys=Patient.patientId)
    doctorId = db.Column(db.Integer, foreign_keys=Doctor.doctorId)
    duration = db.Column(db.Integer)
    cause = db.Column(db.String(200), nullable=True)
    cancelled = db.Column(db.Boolean, default=False)


class ConsultationDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultationId = db.Column(db.Integer, foreign_keys=Consultation.id)
    description = db.Column(db.String(300))
    additionalNotes = db.Column(db.String(300), nullable=True)
    symptoms = db.Column(db.String(120), nullable=True)
    diagnosis = db.Column(db.String(120), nullable=True)
    actualStart = db.Column(db.DateTime, nullable=True)
    actualEnd = db.Column(db.DateTime, nullable=True)
