from flask import Blueprint, request, make_response, jsonify
from app.services import register_user, login_user, create_election, create_candidate, cast_vote

auth_blueprint = Blueprint('main', __name__)

@main_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@main_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

@main_bp.route('/elections', methods=['POST'])
def create_election():
    data = request.get_json()
    return create_election(data)

@main_bp.route('/candidates', methods=['POST'])
def create_candidate():
    data = request.get_json()
    return create_candidate(data)

@main_bp.route('/votes', methods=['POST'])
def cast_vote():
    data = request.get_json()
    return cast_vote(data)

@main_bp.route('/elections', methods=['GET'])
def get_elections():
    return get_elections()

