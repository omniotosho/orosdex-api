from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db
from flask_bcrypt import Bcrypt
import random
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


bcrypt = Bcrypt()

# db = SQLAlchemy(app)

class User(db.Model):
	
	# init users table
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), nullable=False)
	email = db.Column(db.String(150), nullable=False)
	password = db.Column(db.Text, nullable=False)
	avatar = db.Column(db.String(250), nullable=False)
	status = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'name': self.name, 
			'email': self.email,
			'avatar': self.avatar,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# Create new user
	def add_user(_name, _email, _password, _avatar):
		# pass
		hash_password = bcrypt.generate_password_hash(_password.encode('utf8'), 12)
		new_user = User(name=_name, email=_email, password=hash_password.decode('utf8'), avatar=_avatar, status=0)
		db.session.add(new_user)
		db.session.commit()

	# update user avatar
	def update_user_avatar(_id, _avatar):
		user_data = User.query.filter_by(id=_id).first()
		user_data.avatar = _avatar
		db.session.commit()

	# update user name
	def update_user_name(_id, _name):
		user_data = User.query.filter_by(id=_id).first()
		user_data.name = _name
		db.session.commit()

	# update user name
	def update_user_password(_email, _password):
		# pass
		hash_password = bcrypt.generate_password_hash(_password.encode('utf8'), 12)
		user_data = User.query.filter_by(email=_email).first()
		user_data.password = hash_password
		db.session.commit()

	# Fetch all users
	def get_all_users():
		all_users = db.session.query(User).all()
		return [User.json(user) for user in all_users]

	# Fetch all users
	def get_user_by_email(_email):
		user = User.query.filter_by(email=_email).first()
		return User.json(user)

	# Verify email exist!
	def verify_email_exist(_email):
		user = User.query.filter_by(email=_email).first()
		if(user is None): 
			data = {
				"status": "error",
				"message": _email+" was not found, try again!"
			}
		else:
			data = {
				"status": "success",
				"message": _email+" is valid!",
				"reset_link": randomString(22)
			}

		return data

	# Fetch all users
	def get_user_by_user_id(_user_id):
		user = db.session.query(User).filter_by(id=_user_id).first()
		return User.json(user)

	# Authenticate user
	def authenticate_user(_email, _password):
		data = {}
		user = User.query.filter_by(email=_email).first()
		if(user is None):
			return False
		else:
			if(bcrypt.check_password_hash(user.password, _password)):
				return True
			else:
				return False

	# Change user password
	def change_user_password(_user_id, _old_password, _new_password):
		hash_password = bcrypt.generate_password_hash(_new_password.encode('utf8'), 12)
		user = User.query.filter_by(id=_user_id).first()
		if(user is None):
			return False
		else:
			if(bcrypt.check_password_hash(user.password, _old_password)):
				user_to_update = User.query.filter_by(id=_user_id).first()
				user_to_update.password = hash_password.decode('utf8')
				db.session.commit()
				return True
			else:
				return False

	# convert user object to json response
	def __repr__(self):
		user_object = {
			'name': self.name, 
			'email': self.email, 
			'password': self.password,
			'avatar': self.avatar,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}

		return json.dumps(user_object)

# db.create_all()