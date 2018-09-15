from MAPS.api import bp


@bp.route('/patients', methods=['GET'])
def get_users():
    pass


@bp.route('/patients/<int:id>', methods=['GET'])
def get_user(id):
    pass


@bp.route('/patients/<int:id>', methods=['POST'])
def create_user(id):
    pass


@bp.route('/patients/<int:id>', methods=['PUT'])
def update_user(id):
    pass
