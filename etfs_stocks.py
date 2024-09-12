from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class EtfStock(db.Model):
	
	# init users table
	__tablename__ = 'etf_stocks'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	etf_id = db.Column(db.Integer)
	account_type_id = db.Column(db.Integer)
	price = db.Column(db.Float(18, 2))
	units = db.Column(db.Integer)
	total = db.Column(db.Float(18, 2))
	wa_price = db.Column(db.Float(18, 2))
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'user_id': self.user_id,
			'etf_id': self.etf_id,
			'account_type_id': self.account_type_id,
			'price': float(self.price),
			'units': self.units,
			'total': float(self.total),
			'wa_price': float(self.wa_price),
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
			'account_type_id': self.account_type_id,
			'price': float(self.price),
			'units': self.units,
			'total': float(self.total),
			'wa_price': float(self.wa_price),
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return json.dumps(data)

	# init add new
	def add_new(_user_id, _etf_id, _account_type_id, _price, _units, _total, _wa_price):
		# pass
		etf_stock = db.session.query(EtfStock).filter_by(etf_id=_etf_id).first()
		if(etf_stock == None):
			new_etf_stock = EtfStock(user_id=_user_id, etf_id=_etf_id, account_type_id=_account_type_id, price=_price, units=_units, total=_total, wa_price=_wa_price)
			db.session.add(new_etf_stock)
			db.session.commit()

			# create new
			return True
		else:
			total_units = etf_stock.units + _units
			f1 = etf_stock.total
			f2 = _total
			f3 = float(f1) + float(f2)

			new_wa_price =  f3 / total_units

			# update stock balance exist
			etf_stock.price = _price;
			etf_stock.units = total_units;
			etf_stock.total = f3;
			etf_stock.wa_price = new_wa_price;
			db.session.commit()

			return True

	# update
	def update_one(_user_id, _equity_id, _account_type_id, _price, _units, _total, _wa_price):
		pass

	# get by id 
	def get_by_id(_id):
		pass

	# get etf by id 
	def get_by_equity_id(_id):
		pass

	# get all etf
	def get_all():
		pass

	# get all etf
	def stocks_balance(_user_id):
		stock_balances = db.session.query(EtfStock).filter_by(user_id=_user_id).all()
		return [EtfStock.json(stock) for stock in stock_balances]



