from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class Equity(db.Model):
	
	# init users table
	__tablename__ = 'equities'
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
		equity = db.session.query(Equity).filter_by(security=_security).first()
		if(equity == None):
			new_equity = Equity(security=_security, market=_market, sector=_sector, previous_closing_price=_previous_closing_price, open_price=_open_price, close_price=_close_price)
			db.session.add(new_equity)
			db.session.commit()	
			# create new
			return {
				"status": "success",
				"message": _security + " added!"
			}
		else:
			# update existing
			Equity.update_equity(equity.id, _market, _sector, _previous_closing_price, _open_price, _close_price)
			return {
				"status": "success",
				"message": _security + " updated!"
			}

	# update equity
	def update_equity(_id, _market, _sector, _previous_closing_price, _open_price, _close_price):
		# pass
		equity = Equity.query.filter_by(id=_id).first()
		equity.market = _market
		equity.sector = _sector
		equity.previous_closing_price = _previous_closing_price
		equity.open_price = _open_price
		equity.close_price = _close_price
		db.session.commit()
		return True

	# update equity open price
	def update_equity_open_price(_id, _open_price):
		# pass
		equity = Equity.query.filter_by(id=_id).first()
		if(equity is None):
			return {
				"status": "error",
				"message": "Equity not found!"
			}
		else:
			equity.open_price = _open_price
			db.session.commit()
			return {
				"status": "success",
				"message": "update successful!"
			}

	# get equity by id 
	def get_equity_by_id(_id):
		equity = db.session.query(Equity).filter_by(id=_id).first()
		return Equity.json(equity)

	# get equity by name
	def get_equity_by_name(_security):
		equity = db.session.query(Equity).filter_by(security=_security).first()
		if(equity is None):
			return {}
		else:
			return Equity.json(equity)

	# get all equity
	def get_all():
		equities = db.session.query(Equity).all()
		if(equities is None):
			return []
		else:
			return [Equity.json(equity) for equity in equities]




