from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# db = SQLAlchemy(app)

class PasswordReset(db.Model):
	
	# init users table
	__tablename__ = 'password_resets'
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
	def addOne(_email, _link):
		# pass
		already_exist = PasswordReset.query.filter_by(email=_email).first()
		if(already_exist is None):
			activation = PasswordReset(email=_email, link=_link, status=0)
			db.session.add(activation)
			db.session.commit()
		else:
			already_exist.link = _link
			db.session.commit()
		return True

	# activate user account
	def verifyLink(_link):
		# pass
		activation = PasswordReset.query.filter_by(link=_link).first()
		if(activation is None):
			data = {
				"status":  "error",
				"message": "Invalid password reset link"
			}
		else:
			activation.status = 1
			db.session.commit()
			data = {
				"status":  "success",
				"message": "Reset link is valid!"
			}

		return data

