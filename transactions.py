from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class Transaction(db.Model):
	
	# init gl table
	__tablename__ = 'transactions'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	gl_id = db.Column(db.Integer)
	reference = db.Column(db.Text)
	amount = db.Column(db.Float(18, 2))
	transaction_type = db.Column(db.Integer)
	currency = db.Column(db.Integer)
	status = db.Column(db.Integer)
	narration = db.Column(db.Text)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'user_id': self.user_id,
			'gl_id': self.gl_id,
			'reference': self.reference,
			'amount': float(self.amount),
			'transaction_type': self.transaction_type,
			'currency': self.currency,
			'status': self.status,
			'narration': self.narration,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert object to json response
	def __repr__(self):
		user_object = {
			'id': self.id,
			'user_id': self.user_id,
			'gl_id': self.gl_id,
			'reference': self.reference,
			'amount': float(self.amount),
			'transaction_type': self.transaction_type,
			'currency': self.currency,
			'status': self.status,
			'narration': self.narration,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(user_object)

	# debit gl account
	def debit(_user_id, _gl_id, _amount, _narration, _reference):
		transaction = Transaction(user_id=_user_id, gl_id=_gl_id, amount=_amount, transaction_type=1, narration=_narration, reference=_reference, currency=1, status=1)
		db.session.add(transaction)
		db.session.commit()

	# credit gl account
	def credit(_user_id, _gl_id, _amount, _narration, _reference):
		transaction = Transaction(user_id=_user_id, gl_id=_gl_id, amount=_amount, transaction_type=2, narration=_narration, reference=_reference, currency=1, status=1)
		db.session.add(transaction)
		db.session.commit()

	# fetch all transactions
	def get_all():
		all_transactions = db.session.query(Transaction).all()
		return [Transaction.json(transaction) for transaction in all_transactions]

	# fetch all by user_id
	def get_all_by_user_id(_user_id):
		all_transactions = db.session.query(Transaction).filter_by(user_id=_user_id).order_by(Transaction.id.desc()).all()
		return [Transaction.json(transaction) for transaction in all_transactions]

	# fetch all by user_id
	def get_all_by_user_id_and_gl_id(_user_id, _gl_id):
		all_transactions = db.session.query(Transaction).filter_by(user_id=_user_id).filter_by(gl_id=_gl_id).order_by(Transaction.id.desc()).all()
		return [Transaction.json(transaction) for transaction in all_transactions]

	# fetch transaction by ref and user_id
	def get_by_reference_user_id(_reference, _user_id):
		transaction = db.session.query(Transaction).filter_by(reference=_reference).filter_by(user_id=_user_id).first()
		return Transaction.json(transaction)

	# fetch all transactions
	def get_all_by_reference(_reference, _amount):
		all_transactions = db.session.query(Transaction).filter_by(reference=_reference).filter_by(amount=_amount).all()
		return [Transaction.json(transaction) for transaction in all_transactions]

	# fetch transaction by id
	def get_transaction_by_id(_id):
		transaction = db.session.query(Transaction).filter_by(id=_id).first()
		return Transaction.json(transaction)

	def available_balance(_user_id, _gl_id):
		transaction = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=_user_id).filter_by(gl_id=_gl_id).scalar()
		if(transaction is None):
			return 0
		return transaction

	# fetch transaction by gl 
	def get_transaction_by_gl_id(_gl_id):
		all_transactions = db.session.query(Transaction).filter_by(gl_id=_gl_id).all()
		return [Transaction.json(transaction) for transaction in all_transactions]
