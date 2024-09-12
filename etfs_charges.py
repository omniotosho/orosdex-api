from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class EtfCharge(db.Model):
	
	# init users table
	__tablename__ = 'etf_charges'
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
		etf_charge = db.session.query(EtfCharge).filter_by(name=_name).first()
		if(etf_charge == None):
			new_etf_charge = EtfCharge(name=_name, rate=_rate, vat=_vat, total=_total, trade_type=_trade_type)
			db.session.add(new_etf_charge)
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

	# update etf
	def update_etf_charge(_id, _name, _rate, _vat, _total, _trade_type):
		# pass
		etf_charge = EtfCharge.query.filter_by(id=_id).first()
		etf_charge.name = _name
		etf_charge.rate = _rate
		etf_charge.vat = _vat
		etf_charge.total = _total
		etf_charge.trade_type = _trade_type
		db.session.commit()

		data = {
			"status": "success",
			"message": _name+" updated!"
		}
		
		return data

	# get etfs by id 
	def get_etf_charge_by_id(_id):
		etf_charge = db.session.query(EtfCharge).filter_by(id=_id).first()
		return EtfCharge.json(etf_charge)

	# delete etf by id 
	def delete_etf_charge(_id):
		db.session.query(EtfCharge).filter_by(id=_id).delete()
		db.session.commit()
		data = {
			"status": "success",
			"message": "Deleted!"
		}

		return data

	# get all etfs
	def get_all():
		etf_charges = db.session.query(EtfCharge).all()
		if(etf_charges is None):
			return []
		else:
			return [EtfCharge.json(etf) for etf in etf_charges]




