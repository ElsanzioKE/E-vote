from flask import jsonify
from .models import User
from .models import Election
from .models import Candidate
from .models import Vote
from . import db, bcrypt, jwt
from flask_jwt_extended import create_access_token

def register_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        role = data.get('role', 'user')
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.'
        }
        return response_object, 409


def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Logged in successfully', 'access_token': create_access_token(identity=data['email'])})
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.'
        }
        return response_object, 404

def create_election(data):
    election = Election.query.filter_by(name=data['name']).first()
    if not election:
        new_election = Election(
            name=data['name'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        db.session.add(new_election)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Election successfully created.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Election already exists.'
        }
        return response_object, 409

def create_candidate(data):
    candidate = Candidate.query.filter_by(name=data['name']).first()
    if not candidate:
        new_candidate = Candidate(
            name=data['name'],
            election_id=data['election_id']
        )
        db.session.add(new_candidate)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Candidate successfully created.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Candidate already exists.'
        }
        return response_object, 409
    
def cast_vote(data):
    vote = Vote.query.filter_by(user_id=data['user_id'], election_id=data['election_id']).first()
    if not vote:
        new_vote = Vote(
            user_id=data['user_id'],
            election_id=data['election_id'],
            candidate_id=data['candidate_id']
        )
        db.session.add(new_vote)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Vote successfully created.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Vote already exists.'
        }
        return response_object, 409

def get_elections():
    elections = Election.query.all()
    return jsonify(elections)