from MAPS.api import bp


# Get all patients
@bp.route('/patients', methods=['GET'])
def get_users():
    pass


# Get all patients for a doctor
# Reason for route order: https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/
@bp.route('/doctors/patients/<int:id>', methods=['GET'])
def get_users_for_doctor(id):
    pass


# Get a patient by id
@bp.route('/patients/<int:id>', methods=['GET'])
def get_user(id):
    pass


# Create a patient by id
@bp.route('/patients/<int:id>', methods=['POST'])
def create_user(id):
    pass


# Update a patient  by id
@bp.route('/patients/<int:id>', methods=['PUT'])
def update_user(id):
    pass
