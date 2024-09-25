from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class EquityCharge(db.Model):
	
	# init users table
	__tablename__ = 'equities_charges'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	rate = db.Column(db.Float(18, 2))
	vat = db.Column(db.Float(18, 2))
	total = db.Column(db.Float(18, 2))
	trade_type = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'name': self.name,
			'rate': float(self.rate),
			'vat': float(self.vat),
			'total': float(self.total),
			'trade_type': self.trade_type,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return data

	# convert object
	def __repr__(self):
		data = {
			'id': self.id,
			'name': self.name,
			'rate': float(self.rate),
			'vat': float(self.vat),
			'total': float(self.total),
			'trade_type': self.trade_type,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return json.dumps(data)

	# init add new
	def add_new(_name, _rate, _vat, _total, _trade_type):
		# pass
		equity_charge = db.session.query(EquityCharge).filter_by(name=_name).first()
		if(equity_charge == None):
			new_equity_charge = EquityCharge(name=_name, rate=_rate, vat=_vat, total=_total, trade_type=_trade_type)
			db.session.add(new_equity_charge)
			db.session.commit()

			# create new
			return {
				"status": "success",
				"message": _name + " added!"
			}
		else:
			# already exist
			return {
				"status": "success",
				"message": _name + " already exist!"
			}

	# update equity
	def update_equity_charge(_id, _name, _rate, _vat, _total, _trade_type):
		# pass
		equity = EquityCharge.query.filter_by(id=_id).first()
		equity.name = _name
		equity.rate = _rate
		equity.vat = _vat
		equity.total = _total
		equity.trade_type = _trade_type
		db.session.commit()

		data = {
			"status": "success",
			"message": _name+" updated!"
		}
		
		return data

	# get equity by id 
	def get_equity_charge_by_id(_id):
		equities_charge = db.session.query(EquityCharge).filter_by(id=_id).first()
		return EquityCharge.json(equities_charge)

	# get equity by id 
	def delete_equity_charge(_id):
		db.session.query(EquityCharge).filter_by(id=_id).delete()
		db.session.commit()
		data = {
			"status": "success",
			"message": "Deleted!"
		}

		return data

	# get all equity
	def get_all():
		equities_charges = db.session.query(EquityCharge).all()
		if(equities_charges is None):
			return []
		else:
			return [EquityCharge.json(equity) for equity in equities_charges]




