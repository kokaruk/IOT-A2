from MAPS.api import bp


# Get all doctor
@bp.route('/doctors', methods=['GET'])
def get_doctors():
    pass


# Get a doctor by id
@bp.route('/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    pass


# Create a doctor by id
@bp.route('/doctors/<int:id>', methods=['POST'])
def create_doctor(id):
    pass


# Update a doctor  by id
@bp.route('/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    pass


# Delete a doctor  by id
@bp.route('/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    pass


# Get all doctor calendar ids
@bp.route('/doctors/calendars', methods=['GET'])
def get_doctors_calendar_ids():
    pass


# Get a doctor's calendar id by id
@bp.route('/doctors/<int:id>/calendars', methods=['GET'])
def get_doctor_calendar_id(id):
    pass
