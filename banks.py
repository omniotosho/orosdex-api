from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class Bank(db.Model):
	
	# init users table
	__tablename__ = 'banks'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	number = db.Column(db.String(150))
	sort_code = db.Column(db.Text)
	bank_name = db.Column(db.Text)
	owner_name = db.Column(db.Text)
	is_active = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'user_id': self.user_id,
			'number': self.number,
			'sort_code': self.sort_code,
			'bank_name': self.bank_name,
			'owner_name': self.owner_name,
			'is_active': self.is_active,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert user object to json response
	def __repr__(self):
		user_object = {
			'id': self.id,
			'user_id': self.user_id,
			'number': self.number,
			'sort_code': self.sort_code,
			'bank_name': self.bank_name,
			'owner_name': self.owner_name,
			'is_active': self.is_active,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(user_object)

	# init bank data
	def init_user_bank(_user_id):
		# pass
		bank = Bank(user_id=_user_id, is_active=1)
		db.session.add(bank)
		db.session.commit()
		return True

	# update bank data
	def update_user_bank(_user_id, _number, _sort_code, _bank_name, _owner_name):
		# pass
		bank = Bank.query.filter_by(user_id=_user_id).first()
		bank.number = _number
		bank.sort_code = _sort_code
		bank.bank_name = _bank_name
		bank.owner_name = _owner_name
		bank.is_active = 1
		db.session.commit()
		return True

	# get user bank
	def get_bank_by_user_id(_user_id):
		bank = db.session.query(Bank).filter_by(user_id=_user_id).first()
		return Bank.json(bank)

	# delete user bank
	def delete_bank(_user_id):
		bank = db.session.query(Bank).filter_by(user_id=_user_id).delete()
		db.session.commit()
		return True

	# activate user account
	def activate_account(_user_id):
		# pass
		bank = Bank.query.filter_by(user_id=_user_id).first()
		bank.status = 1
		db.session.commit()
		return True

