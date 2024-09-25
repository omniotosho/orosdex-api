from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class EtfTransaction(db.Model):
	
	# init users table
	__tablename__ = 'etf_transactions'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	etf_id = db.Column(db.Integer)
	transaction_id = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'user_id': self.user_id,
			'etf_id': self.etf_id,
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
			'etf_id': self.etf_id,
			'transaction_id': self.transaction_id,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return json.dumps(data)

	# init add new
	def add_new(_user_id, _etf_id, _transaction_id):
		new_etf_transaction = EtfTransaction(user_id=_user_id, etf_id=_etf_id, transaction_id=_transaction_id)
		db.session.add(new_etf_transaction)
		db.session.commit()

	# get by etf id
	def get_by_etf_id(_etf_id):
		all_etfs_transactions = db.session.query(EtfTransaction).filter_by(etf_id=_etf_id).all()
		return [EtfTransaction.json(etf_transaction) for etf_transaction in all_etfs_transactions]

	# get by etf ids
	def get_by_etf_ids(_etf_id):
		all_etfs_transactions = db.session.query(EtfTransaction.transaction_id).filter_by(etf_id=_etf_id).distinct()
		return [EtfTransaction.json(etf_transaction) for etf_transaction in all_etfs_transactions]

	# get by id 
	def get_by_id(_id):
		etf_transaction = db.session.query(EtfTransaction).filter_by(user_id=_user_id).first()
		return EtfTransaction.json(etf_transaction)

	# get all etf by user id
	def get_by_user_id(_user_id):
		all_etfs_transactions = db.session.query(EtfTransaction).filter_by(user_id=_user_id).all()
		return [EtfTransaction.json(etf_transaction) for etf_transaction in all_etfs_transactions]
