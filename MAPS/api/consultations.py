from MAPS.api import bp
from MAPS import db


# Get all consultations for a particular doctor
# Reason for route order: https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/
@bp.route('/doctors/<int:id>/consultations', methods=['GET'])
def get_consultations_doctor(id):
    pass


# Get all consultations for a particular patient
# Reason for route order: https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/
@bp.route('/patients/<int:id>/consultations', methods=['GET'])
def get_consultations_patient(id):
    pass


# Create a consultation
@bp.route('/consultations', methods=['POST'])
def create_consultation():
    # get all information from body
    pass


# Create a consultation by id
@bp.route('/consultations/<int:id>', methods=['PUT'])
def update_consultation(id):
    # get updated information from body
    pass


# Delete a consultation by id
@bp.route('/consultations/<int:id>', methods=['DELETE'])
def delete_consultation(id):
    pass


# Get a consultationDetail for a particular consultation
@bp.route('/consultations/details/<int:id>', methods=['GET'])
def get_consultation_detail(id):
    pass


# Update a consultationDetail for a particular consultation
@bp.route('/consultations/details/<int:id>', methods=['PUT'])
def update_consultation_detail(id):
    # get updated information from body
    pass


# Delete a consultationDetail for a particular consultation
@bp.route('/consultations/details/<int:id>', methods=['DELETE'])
def delete_consultation_detail(id):
    pass


# Get all the consultationDetails for a particular consultation
@bp.route('/consultations/<int:id>/details', methods=['GET'])
def get_consultations_details(id):
    pass
