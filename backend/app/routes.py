from flask import Blueprint, request, make_response, jsonify
from .services import register_user, login_user, create_election, create_candidate, cast_vote, get_elections, get_vote_counts
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User
from .extensions import db

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
    email = data['email']
    admin_user = User.query.filter_by(email=email).first()
    if admin_user:
        admin_user.role = 'admin'
        db.session.commit()
        return jsonify({'message': f'User {email} is now an admin'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@main_bp.route('/elections', methods=['POST'])
@jwt_required()
def create_election_route():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'message': 'Admin access required!'}), 403
    data = request.get_json()
    return create_election(data)

@main_bp.route('/candidates', methods=['POST'])
@jwt_required()
def create_candidate_route():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'message': 'Admin access required!'}), 403
    data = request.get_json()
    return create_candidate(data)


@main_bp.route('/votes', methods=['POST'])
@jwt_required()
def cast_vote_route():
    identity = get_jwt_identity()
    data = request.get_json()
    return cast_vote(data, identity)

@main_bp.route('/elections', methods=['GET'])
@jwt_required()
def get_elections_route():
    return get_elections()

@main_bp.route('/vote_counts', methods=['GET'])
@jwt_required()
def get_vote_counts_route():
    return get_vote_counts()


