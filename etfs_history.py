from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class EtfHistory(db.Model):
	
	# init users table
	__tablename__ = 'etf_history'
	id = db.Column(db.Integer, primary_key=True)
	security = db.Column(db.Text)
	market = db.Column(db.Text)
	sector = db.Column(db.Text)
	previous_open_price = db.Column(db.Float(18, 2))
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
			'previous_open_price': self.previous_open_price,
			'open_price': self.open_price,
			'close_price': self.close_price,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return data

	# convert object
	def __repr__(self):
		data = {
			'id': self.id,
			'security': self.security,
			'market': self.market,
			'sector': self.sector,
			'previous_open_price': self.previous_open_price,
			'open_price': self.open_price,
			'close_price': self.close_price,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return json.dumps(data)

	# init add new
	def add_new(_security, _market, _sector, _previous_open_price, _open_price, _close_price):
		# pass
		etf = EtfHistory(security=_security, market=_market, sector=_sector, previous_open_price=_previous_open_price, open_price=_open_price, close_price=_close_price)
		db.session.add(etf)
		db.session.commit()
		return True

	# get all history
	def get_all():
		etf_history = db.session.query(EtfHistory).all()
		return [EtfHistory.json(etf) for etf in etf_history]


