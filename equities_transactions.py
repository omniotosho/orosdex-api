from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class EquityTransaction(db.Model):
	
	# init users table
	__tablename__ = 'equities_transactions'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	equity_id = db.Column(db.Integer)
	transaction_id = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'user_id': self.user_id,
			'equity_id': self.equity_id,
			'transaction_id': self.transaction_id,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return data

	# convert object
	def __repr__(self):
		data = {
			'id': self.id,
			'user_id': self.user_id,
			'equity_id': self.equity_id,
			'transaction_id': self.transaction_id,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return json.dumps(data)

	# init add new
	def add_new(_user_id, _equity_id, _transaction_id):
		new_equity_transaction = EquityTransaction(user_id=_user_id, equity_id=_equity_id, transaction_id=_transaction_id)
		db.session.add(new_equity_transaction)
		db.session.commit()

	# get by equity id
	def get_by_equity_id(_equity_id):
		all_equities_transactions = db.session.query(EquityTransaction).filter_by(equity_id=_equity_id).all()
		return [EquityTransaction.json(equity_transaction) for equity_transaction in all_equities_transactions]

	# get by equity id
	def get_by_equity_ids(_equity_id):
		all_equities_transactions = db.session.query(EquityTransaction.transaction_id).filter_by(equity_id=_equity_id).distinct()
		return [EquityTransaction.json(equity_transaction) for equity_transaction in all_equities_transactions]

	# get by id 
	def get_by_id(_id):
		equity_transaction = db.session.query(EquityTransaction).filter_by(user_id=_user_id).first()
		return EquityTransaction.json(equity_transaction)

	# get all equity by user id
	def get_by_user_id(_user_id):
		all_equities_transactions = db.session.query(EquityTransaction).filter_by(user_id=_user_id).all()
		return [EquityTransaction.json(equity_transaction) for equity_transaction in all_equities_transactions]
