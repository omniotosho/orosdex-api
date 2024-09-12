from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class Profile(db.Model):
	
	# init profiles table
	__tablename__ = 'profiles'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	gender = db.Column(db.Integer)
	bvn = db.Column(db.String)
	phone = db.Column(db.String)
	address = db.Column(db.Text)
	occupation = db.Column(db.Integer)
	date_of_birth = db.Column(db.String)
	state_of_origin = db.Column(db.Integer)
	lga = db.Column(db.Integer)
	nationality = db.Column(db.Integer)
	description = db.Column(db.Text)
	status = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'user_id': self.user_id,
			'gender': self.gender,
			'bvn': self.bvn,
			'phone': self.phone,
			'address': self.address,
			'occupation': self.occupation,
			'date_of_birth': self.date_of_birth,
			'state_of_origin': self.state_of_origin,
			'lga': self.lga,
			'nationality': self.nationality,
			'description': self.description,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert user object to json response
	def __repr__(self):
		user_object = {
			'id': self.id,
			'user_id': self.user_id,
			'gender': self.gender,
			'bvn': self.bvn,
			'phone': self.phone,
			'address': self.address,
			'occupation': self.occupation,
			'date_of_birth': self.date_of_birth,
			'state_of_origin': self.state_of_origin,
			'lga': self.lga,
			'nationality': self.nationality,
			'description': self.description,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(user_object)

	# init profile for user
	def init_user_profile(_user_id):
		# pass
		init_profile = Profile(user_id=_user_id)
		db.session.add(init_profile)
		db.session.commit()

	# update profile information
	def update_user_profile(_user_id, _gender, _bvn, _phone, _address, _occupation, _date_of_birth, _state_of_origin, _lga, _nationality, _description):
		# pass
		user_data = Profile.query.filter_by(user_id=_user_id).first()
		user_data.gender = _gender
		user_data.bvn = _bvn
		user_data.phone = _phone
		user_data.address = _address
		user_data.occupation = _occupation
		user_data.date_of_birth = _date_of_birth
		user_data.state_of_origin = _state_of_origin
		user_data.lga = _lga
		user_data.nationality = _nationality
		user_data.description = _description
		db.session.commit()

	# get user profile
	def get_user_profile(_user_id):
		# pass
		profile = db.session.query(Profile).filter_by(user_id=_user_id).first()
		if(profile is None):
			profile = {}
			return profile
		else:
			return Profile.json(profile)
	