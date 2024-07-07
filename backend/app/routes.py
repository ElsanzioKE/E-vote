from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .services import register_user, login_user, create_election, create_candidate, cast_vote, get_elections, get_vote_counts
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import User
from .extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('layout.html')

@main_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        data = request.get_json()
        if 'username' in data:
            return register_user(data)
        else:
            return login_user(data)
    return render_template('login.html')

@main_bp.route('/logout')
@jwt_required()
def logout():
    # Logic for logging out the user
    return redirect(url_for('main.index'))

@main_bp.route('/create_admin', methods=['POST'])
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

@main_bp.route('/elections', methods=['POST', 'GET'])
@jwt_required()
def elections():
    if request.method == 'POST':
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        data = request.get_json()
        return create_election(data)
    elif request.method == 'GET':
        return get_elections()

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

@main_bp.route('/vote_counts', methods=['GET'])
@jwt_required()
def get_vote_counts_route():
    return get_vote_counts()
    return render_template('seeresults.html')

@main_bp.route('/admin_dashboard')
@jwt_required()
def admin_dashboard():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return redirect(url_for('main.index'))
    return render_template('admin_dashboard.html')

@main_bp.route('/cast_vote/<int:election_id>')
@jwt_required()
def cast_vote_page(election_id):
    # Fetch candidates for the given election_id
    # candidates = ...
    return render_template('cast_vote.html', election_id=election_id, candidates=candidates)
