from flask import Blueprint, request, make_response, jsonify
from .services import register_user, login_user, create_election, create_candidate, cast_vote, get_elections
from flask_jwt_extended import jwt_required, get_jwt_identity
main_bp = Blueprint('main', __name__)

@main_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@main_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

@main_bp.route('/auth/create_admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    data['role'] = 'admin'
    return register_user(data)

@main_bp.route('/elections', methods=['POST'])
@jwt_required()
def create_election():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'message': 'Admin access required!'}), 403
    data = request.get_json()
    return create_election(data)

@main_bp.route('/candidates', methods=['POST'])
@jwt_required()
def create_candidate():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'message': 'Admin access required!'}), 403
    data = request.get_json()
    return create_candidate(data)

@main_bp.route('/votes', methods=['POST'])
@jwt_required()
def cast_vote():
    data = request.get_json()
    return cast_vote(data)

@main_bp.route('/elections', methods=['GET'])
@jwt_required()
def get_elections_route():
    return get_elections()

