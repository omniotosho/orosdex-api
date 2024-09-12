from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class Customer(db.Model):
	
	# init users table
	__tablename__ = 'customers'
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(150))
	acct_code = db.Column(db.Text)
	passport = db.Column(db.Text, nullable=True)
	bvn = db.Column(db.Text, nullable=True)
	email = db.Column(db.Text, nullable=True)
	state_of_origin = db.Column(db.Text, nullable=True)
	gender = db.Column(db.Text, nullable=True)
	local_govt = db.Column(db.Text, nullable=True)
	date_of_birth = db.Column(db.Text, nullable=True)
	nationality = db.Column(db.Text, nullable=True)
	phone_number = db.Column(db.Text, nullable=True)
	occupation = db.Column(db.Text, nullable=True)
	description = db.Column(db.Text, nullable=True)
	home_address = db.Column(db.Text, nullable=True)
	business_address = db.Column(db.Text, nullable=True)
	status = db.Column(db.Integer, nullable=True)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# SQL Alchemy return to Json
	def json(self):
		json_data = {
			'id': self.id,
			'full_name': self.full_name,
			'acct_code': self.acct_code,
			'passport': self.passport,
			'bvn': self.bvn,
			'email': self.email,
			'state_of_origin': self.state_of_origin,
			'gender': self.gender,
			'local_govt': self.local_govt,
			'date_of_birth': self.date_of_birth,
			'nationality': self.nationality,
			'phone_number': self.phone_number,
			'occupation': self.occupation,
			'description': self.description,
			'home_address': self.home_address,
			'business_address': self.business_address,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json_data

	# convert user object to json response
	def __repr__(self):
		customer_object = {
			'id': self.id,
			'full_name': self.full_name,
			'acct_code': self.acct_code,
			'passport': self.passport,
			'bvn': self.bvn,
			'email': self.email,
			'state_of_origin': self.state_of_origin,
			'gender': self.gender,
			'local_govt': self.local_govt,
			'date_of_birth': self.date_of_birth,
			'nationality': self.nationality,
			'phone_number': self.phone_number,
			'occupation': self.occupation,
			'description': self.description,
			'home_address': self.home_address,
			'business_address': self.business_address,
			'status': self.status,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(customer_object)

	# fetch all customer
	def all_customer():
		customers = db.session.query(Customer).all()
		return [Customer.json(customer) for customer in customers]

	# fetch one customer
	def one_customer(_id):
		customer = Customer.query.filter_by(id=_id).first()
		return Customer.json(customer)

	# add customer data
	def add_customer(_passport, _full_name, _acct_code, _bvn, _email, _state_of_origin, _gender, _local_govt, _date_of_birth, _nationality, _phone_number, _occupation, _description, _home_address, _business_address):
		# pass
		customer_exist = db.session.query(Customer).filter_by(acct_code=_acct_code).filter_by(full_name=_full_name).first()
		if(customer_exist == None):
			customer = Customer(passport = _passport, full_name = _full_name, acct_code = _acct_code, bvn = _bvn, email = _email, state_of_origin = _state_of_origin, gender = _gender, local_govt = _local_govt, date_of_birth = _date_of_birth, nationality = _nationality, phone_number = _phone_number, occupation = _occupation, description = _description, home_address = _home_address, business_address = _business_address, status = 1)
			db.session.add(customer)
			db.session.commit()
			return {
				"status": "success",
				"message": _full_name + " record created successfully!"
			}
		else:
			return {
				"status": "error",
				"message": _full_name + " already exist successfully!"
			}

	# update customer data
	def update_customer(_id, _passport, _full_name, _acct_code, _bvn, _email, _state_of_origin, _gender, _local_govt, _date_of_birth, _nationality, _phone_number, _occupation, _description, _home_address, _business_address):
		customer = Customer.query.filter_by(id=_id).first()
		customer.full_name = _full_name
		customer.acct_code = _acct_code
		customer.passport = _passport
		customer.bvn = _bvn
		customer.email = _email
		customer.state_of_origin = _state_of_origin
		customer.gender = _gender
		customer.local_govt = _local_govt
		customer.date_of_birth = _date_of_birth
		customer.nationality = _nationality
		customer.phone_number = _phone_number
		customer.occupation = _occupation
		customer.description = _description
		customer.home_address = _home_address
		customer.business_address = _business_address
		customer.status = 1
		db.session.commit()
		return {
			"status": "success",
			"message": _full_name + " record created successfully!"
		}

	# delete customer data
	def delete_customer(_id):
		customer = db.session.query(Customer).filter_by(id=_id).delete()
		db.session.commit()
		return True

	# activate customer account
	def activate_account(_id):
		# pass
		customer = Customer.query.filter_by(id=_id).first()
		customer.status = 2
		db.session.commit()
		return True

