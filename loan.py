from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db
from customer import *

# db = SQLAlchemy(app)

class Loan(db.Model):
	
	# init users table
	__tablename__ = 'loans'
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer)
	description = db.Column(db.Text, nullable=True)
	principal = db.Column(db.Float(18, 2))
	interest = db.Column(db.Float(18, 2))
	amount = db.Column(db.Float(18, 2))
	daily_payment = db.Column(db.Float(18, 2))
	weekly_payment = db.Column(db.Float(18, 2))
	monthly_payment = db.Column(db.Float(18, 2))
	daily_duration = db.Column(db.Integer)
	weekly_duration = db.Column(db.Integer)
	monthly_duration = db.Column(db.Integer)
	percentage = db.Column(db.Float(18, 2))
	gl_id = db.Column(db.Integer)
	status = db.Column(db.Integer)
	loan_type = db.Column(db.Integer)
	loan_start_date = db.Column(db.DateTime())
	loan_end_date = db.Column(db.DateTime())
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'customer_id': self.customer_id,
			'description': self.description,
			'principal': float(self.principal),
			'interest': float(self.interest),
			'amount': float(self.amount),
			'daily_payment': float(self.daily_payment),
			'weekly_payment': float(self.weekly_payment),
			'monthly_payment': float(self.monthly_payment),
			'daily_duration': self.daily_duration,
			'weekly_duration': self.weekly_duration,
			'monthly_duration': self.monthly_duration,
			'percentage': float(self.percentage),
			'gl_id': self.gl_id,
			'status': self.status,
			'loan_start_date': self.loan_start_date,
			'loan_end_date': self.loan_end_date,
			'customer': self.getCustomerInfo(self.customer_id),
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return data

	# convert object
	def __repr__(self):
		data = {
			'id': self.id,
			'customer_id': self.customer_id,
			'description': self.description,
			'principal': float(self.principal),
			'interest': float(self.interest),
			'amount': float(self.amount),
			'daily_payment': float(self.daily_payment),
			'weekly_payment': float(self.weekly_payment),
			'monthly_payment': float(self.monthly_payment),
			'daily_duration': self.daily_duration,
			'weekly_duration': self.weekly_duration,
			'monthly_duration': self.monthly_duration,
			'percentage': float(self.percentage),
			'gl_id': self.gl_id,
			'status': self.status,
			'loan_start_date': self.loan_start_date,
			'loan_end_date': self.loan_end_date,
			'customer': self.getCustomerInfo(self.customer_id),
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(data)

	# init add new
	def add_loan(_customer_id, _description, _principal, _interest, _amount, _daily_payment, _weekly_payment, _monthly_payment, _daily_duration, _weekly_duration, _monthly_duration, _percentage, _gl_id, _status, _loan_type, _loan_start_date, _loan_end_date):
		# pass
		new_loan = Loan(customer_id = _customer_id, description = _description, principal = _principal, interest = _interest, amount = _amount, daily_payment = _daily_payment, weekly_payment = _weekly_payment, monthly_payment = _monthly_payment, daily_duration = _daily_duration, weekly_duration = _weekly_duration, monthly_duration = _monthly_duration, percentage = _percentage, gl_id = _gl_id, status = _status, loan_type = _loan_type, loan_start_date = _loan_start_date, loan_end_date = _loan_end_date)
		db.session.add(new_loan)
		db.session.commit()

		# create new
		return {
			"status": "success",
			"message": "Loan has been created successfully!"
		}

	# update loan
	def update_loan(_id, _customer_id, _description, _principal, _interest, _amount, _daily_payment, _weekly_payment, _monthly_payment, _daily_duration, _weekly_duration, _monthly_duration, _percentage, _gl_id, _status, _loan_type, _loan_start_date, _loan_end_date):
		# pass
		loan = Loan.query.filter_by(id=_id).first()
		loan.description = _description
		loan.principal = _principal
		loan.interest = _interest
		loan.amount = _amount
		loan.daily_payment = _daily_payment
		loan.weekly_payment = _weekly_payment
		loan.monthly_payment = _monthly_payment
		loan.daily_duration = _daily_duration
		loan.weekly_duration = _weekly_duration
		loan.monthly_duration = _monthly_duration
		loan.percentage = _percentage
		loan.gl_id = _gl_id
		loan.status = _status
		loan.loan_type = _loan_type
		loan.loan_start_date = _loan_start_date
		loan.loan_end_date = _loan_end_date
		db.session.commit()

		data = {
			"status": "success",
			"message": "Loan updated!"
		}
		
		return data

	# get loan by id 
	def one_loan(_id):
		loan = db.session.query(Loan).filter_by(id=_id).first()
		return Loan.json(loan)

	# customer id
	def one_loan_by_customer_id(customer_id):
		loans = db.session.query(Loan).filter_by(customer_id=customer_id).all()
		if(loans is None):
			return []
		else:
			return [Loan.json(loan) for loan in loans]

	# delete loan by id 
	def delete_loan(_id):
		db.session.query(Loan).filter_by(id=_id).delete()
		db.session.commit()
		data = {
			"status": "success",
			"message": "Deleted!"
		}

		return data

	# get all loan
	def all_loan():
		loans = db.session.query(Loan).all()
		if(loans is None):
			return []
		else:
			return [Loan.json(loan) for loan in loans]

	# get customer info
	def getCustomerInfo(self, customer_id):
		return Customer.one_customer(customer_id)




