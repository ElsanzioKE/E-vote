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
        access_token = create_access_token(identity={'username': user.username, 'email': user.email, 'role': user.role})
        return jsonify({'token': access_token}), 200
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.'
        }
        return response_object, 404

from datetime import datetime

def create_election(data):
    election = Election.query.filter_by(name=data['name']).first()
    if not election:
        new_election = Election(
            name=data['name'],
            start_date=datetime.fromisoformat(data['start_date'].replace("Z", "")),
            end_date=datetime.fromisoformat(data['end_date'].replace("Z", ""))
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
    
def cast_vote(data, identity):
    # Find the voter based on the JWT identity
    voter = User.query.filter_by(email=identity['email']).first()
    if not voter:
        return {"status": "fail", "message": "Voter not found."}, 404

    # Find the election based on the provided election name
    election = Election.query.filter_by(name=data['election_name']).first()
    if not election:
        return {"status": "fail", "message": "Election not found."}, 404

    # Find the candidate based on the provided candidate name and election ID
    candidate = Candidate.query.filter_by(name=data['candidate_name'], election_id=election.id).first()
    if not candidate:
        return {"status": "fail", "message": "Candidate not found."}, 404

    # Check if the voter has already voted in this election
    existing_vote = Vote.query.filter_by(user_id=voter.id, election_id=election.id).first()
    if existing_vote:
        return {"status": "fail", "message": "Voter has already voted in this election."}, 409

    # Create a new vote
    new_vote = Vote(
        user_id=voter.id,
        election_id=election.id,
        candidate_id=candidate.id
    )
    db.session.add(new_vote)
    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Vote successfully cast.'
    }
    return response_object, 201

def get_elections():
    elections = Election.query.all()
    elections_list = []
    for election in elections:
        elections_list.append({
            'name': election.name,
            'start_date': election.start_date,
            'end_date': election.end_date
        })
    response_object = {
        'status': 'success',
        'elections': elections_list
    }
    return response_object, 200

def get_vote_counts():
    elections = Election.query.all()
    result = []
    
    for election in elections:
        candidates = Candidate.query.filter_by(election_id=election.id).all()
        candidate_list = []
        
        for candidate in candidates:
            vote_count = Vote.query.filter_by(candidate_id=candidate.id).count()
            candidate_list.append({
                'name': candidate.name,
                'vote_count': vote_count
            })
        
        result.append({
            'election_name': election.name,
            'candidates': candidate_list
        })
    
    response_object = {
        'status': 'success',
        'elections': result
    }
    return response_object, 200
