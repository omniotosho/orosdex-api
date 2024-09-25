from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import db

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# db = SQLAlchemy(app)

class Activation(db.Model):
	
	# init users table
	__tablename__ = 'activations'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), nullable=False)
	link = db.Column(db.Text, nullable=False)
	status = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'email': self.email, 
			'link': self.link,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert user object to json response
	def __repr__(self):
		user_object = {
			'id': self.id,
			'email': self.email, 
			'link': self.link,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(user_object)

	# add new link
	def init_user_activation(_email):
		# pass
		hash_link = bcrypt.generate_password_hash(_email.encode('utf8'), 12)
		activation = Activation(email=_email, link=hash_link.decode('utf8'), status=0)
		db.session.add(activation)
		db.session.commit()
		return hash_link.decode('utf8')

	# activate user account
	def activate_account(_activation_link):
		# pass
		activation = Activation.query.filter_by(link=_activation_link).first()
		if(activation is None):
			data = {
				"status":  "error",
				"message": "invalid activation link"
			}
		else:
			activation.status = 1
			db.session.commit()
			data = {
				"status":  "success",
				"message": "Account has been activated"
			}

		return data

