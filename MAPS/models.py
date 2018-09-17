from MAPS import db, ma


class Person(db.Model):
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
    doctors = db.relationship("Doctor", lazy='dynamic')
    patients = db.relationship("Patient", lazy='dynamic')


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personId = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    specialization = db.Column(db.String(120))
    consultations = db.relationship("Consultation", lazy='dynamic')


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personId = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
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
        fields = ('first_name', 'second_name', 'last_name', 'dob', 'gender', 'address',
                  'email', 'phone', 'medicareNumber', 'previousDoctor', 'previousClinic')


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    condition = db.Column(db.String(120), nullable=True)


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medication = db.Column(db.String(120), nullable=True)


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment = db.Column(db.DateTime)
    patientId = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctorId = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    duration = db.Column(db.Integer)
    cause = db.Column(db.String(200), nullable=True)
    cancelled = db.Column(db.Boolean, default=False)
    consultationDetails = db.relationship("ConsultationDetails")

class ConsultationDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultationId = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=False)
    description = db.Column(db.String(300))
    additionalNotes = db.Column(db.String(300), nullable=True)
    symptoms = db.Column(db.String(120), nullable=True)
    diagnosis = db.Column(db.String(120), nullable=True)
    actualStart = db.Column(db.DateTime, nullable=True)
    actualEnd = db.Column(db.DateTime, nullable=True)
