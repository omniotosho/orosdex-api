from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class Etf(db.Model):
	
	# init users table
	__tablename__ = 'etfs'
	id = db.Column(db.Integer, primary_key=True)
	security = db.Column(db.Text)
	market = db.Column(db.Text)
	sector = db.Column(db.Text)
	previous_closing_price = db.Column(db.Float(18, 2))
	open_price = db.Column(db.Float(18, 2))
	close_price = db.Column(db.Float(18, 2))
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'security': self.security,
			'market': self.market,
			'sector': self.sector,
			'previous_closing_price': float(self.previous_closing_price),
			'open_price': float(self.open_price),
			'close_price': float(self.close_price),
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return data

	# convert object
	def __repr__(self):
		data = {
			'id': self.id,
			'security': self.security,
			'market': self.market,
			'sector': self.sector,
			'previous_closing_price': float(self.previous_closing_price),
			'open_price': float(self.open_price),
			'close_price': float(self.close_price),
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}
		return json.dumps(data)

	# init add new
	def add_new(_security, _market, _sector, _previous_closing_price, _open_price, _close_price):
		# pass
		etf = db.session.query(Etf).filter_by(security=_security).first()
		if(etf == None):
			new_etf = Etf(security=_security, market=_market, sector=_sector, previous_closing_price=_previous_closing_price, open_price=_open_price, close_price=_close_price)
			db.session.add(new_etf)
			db.session.commit()	
			# create new
			return {
				"status": "success",
				"message": _security + " added!"
			}
		else:
			# update existing
			Etf.update_etf(etf.id, _market, _sector, _previous_closing_price, _open_price, _close_price)
			return {
				"status": "success",
				"message": _security + " updated!"
			}

	# update etfs
	def update_etf(_id, _market, _sector, _previous_closing_price, _open_price, _close_price):
		# pass
		etf = Etf.query.filter_by(id=_id).first()
		etf.market = _market
		etf.sector = _sector
		etf.previous_closing_price = _previous_closing_price
		etf.open_price = _open_price
		etf.close_price = _close_price
		db.session.commit()
		return True

	# update etf open price
	def update_etf_open_price(_id, _open_price):
		# pass
		etf = Etf.query.filter_by(id=_id).first()
		if(etf is None):
			return {
				"status": "error",
				"message": "ETF not found!"
			}
		else:
			etf.open_price = _open_price
			db.session.commit()
			return {
				"status": "success",
				"message": "update successful!"
			}

	# get etf by id 
	def get_etf_by_id(_id):
		etf = db.session.query(Etf).filter_by(id=_id).first()
		return Etf.json(etf)

	# get etf by name
	def get_etf_by_name(_security):
		etf = db.session.query(Etf).filter_by(security=_security).first()
		if(etf is None):
			return {}
		else:
			return Etf.json(etf)

	# get all etf
	def get_all():
		etfs = db.session.query(Etf).all()
		if(etfs is None):
			return []
		else:
			return [Etf.json(etf) for etf in etfs]