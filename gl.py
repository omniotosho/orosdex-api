from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db
from account_type import *

# db = SQLAlchemy(app)

class Gl(db.Model):
	
	# init gl table
	__tablename__ = 'gls'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	account_type_id = db.Column(db.Integer)
	book_balance = db.Column(db.Float(18, 2))
	cleared_balance = db.Column(db.Float(18, 2))
	status = db.Column(db.Integer)
	description = db.Column(db.Text)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'user_id': self.user_id,
			'account_type_id': self.account_type_id,
			'book_balance': float(self.book_balance),
			'cleared_balance': float(self.cleared_balance),
			'description': self.description,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert object to json response
	def __repr__(self):
		user_object = {
			'id': self.id,
			'user_id': self.user_id,
			'account_type_id': self.account_type_id,
			'book_balance': float(self.book_balance),
			'cleared_balance': float(self.cleared_balance),
			'description': self.description,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(user_object)

	# init gl for instant deposit
	def init_gl_account(_user_id, _account_type_id):
		# pass
		gl = Gl(user_id=_user_id, account_type_id=_account_type_id, status=1, description='CLIENT INSTANT DEPOSIT', cleared_balance=0, book_balance=0)
		db.session.add(gl)
		db.session.commit()

	# add new gl
	def add_new(_user_id, _account_type_id, _description):
		# get all gl
		gl_exist = db.session.query(Gl).filter_by(user_id=_user_id).filter_by(account_type_id=_account_type_id).first()
		if(gl_exist is None):
			gl = Gl(user_id=_user_id, account_type_id=_account_type_id, status=1, description=_description, cleared_balance=0, book_balance=0)
			db.session.add(gl)
			db.session.commit()

	# fetch all gl
	def get_all():
		# get all gl
		gls = db.session.query(Gl).join(AccountType, Gl.account_type_id == AccountType.id).all()

		return [Gl.json(gl) for gl in gls]

	# get one gl
	def get_one(_id):
		gl = db.session.query(Gl).filter_by(id=_id).first()
		return Gl.json(gl)

	# get one gl by user id
	def get_all_user_gl(_user_id):
		gls = db.session.query(Gl).filter_by(user_id=_user_id).all()
		return [Gl.json(gl) for gl in gls]

	# get one gl by user id
	def get_user_gl_by_type(_user_id, _account_type_id):
		gl = db.session.query(Gl).filter_by(user_id=_user_id).filter_by(account_type_id=_account_type_id).first()
		if(gl is None):
			return {}
		else:
			return Gl.json(gl)

	# update one gl
	def update_one(_id, _book_balance, _cleared_balance):
		gl = db.session.query(Gl).filter_by(id=_id).first()
		if(gl is None):
			return False
		else:
			gl.cleared_balance = _cleared_balance
			gl.book_balance = _book_balance
			db.session.commit()
			return True

	# delete gl
	def delete_one(_id):
		gl = db.session.query(Gl).filter_by(id=_id).delete()
		db.session.commit()
		return True
