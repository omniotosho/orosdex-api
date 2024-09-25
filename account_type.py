from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class AccountType(db.Model):
	
	# init account type table
	__tablename__ = 'account_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	status = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'name': self.name,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert object to json response
	def __repr__(self):
		user_object = {
			'id': self.id,
			'name': self.name,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(user_object)
	
	# add account type for instant use
	def add_account_type(_name):
		account_type = AccountType(name=_name, status=1)
		db.session.add(account_type)
		db.session.commit()

	# update account type1
	def update_account_type(_id, _name):
		account_type = db.session.query(AccountType).filter_by(id=_id).first()
		account_type.name = _name
		db.session.commit()

	# fetch all account type
	def fetch_all_accounts():
		accounts = db.session.query(AccountType).all()
		return [AccountType.json(account) for account in accounts]

	# fetch one account type
	def fetch_one_account(_id):
		account = db.session.query(AccountType).filter_by(id=_id).first()
		return AccountType.json(account)

	# delete account
	def delete_account(_id):
		account = db.session.query(AccountType).filter_by(id=_id).delete()
		db.session.commit()
		return True