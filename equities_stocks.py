from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class EquityStock(db.Model):
	
	# init users table
	__tablename__ = 'equities_stocks'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	equity_id = db.Column(db.Integer)
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
			'equity_id': self.equity_id,
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
			'equity_id': self.equity_id,
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
	def add_new(_user_id, _equity_id, _account_type_id, _price, _units, _total, _wa_price):
		# pass
		equity_stock = db.session.query(EquityStock).filter_by(equity_id=_equity_id).first()
		if(equity_stock == None):
			new_equity_stock = EquityStock(user_id=_user_id, equity_id=_equity_id, account_type_id=_account_type_id, price=_price, units=_units, total=_total, wa_price=_wa_price)
			db.session.add(new_equity_stock)
			db.session.commit()

			# create new
			return True
		else:
			total_units = equity_stock.units + _units
			f1 = equity_stock.total
			f2 = _total
			f3 = float(f1) + float(f2)

			new_wa_price =  f3 / total_units

			# update stock balance exist
			equity_stock.price = _price;
			equity_stock.units = total_units;
			equity_stock.total = f3;
			equity_stock.wa_price = new_wa_price;
			db.session.commit()

			return True

	# update
	def update_one(_user_id, _equity_id, _account_type_id, _price, _units, _total, _wa_price):
		pass

	# get by id 
	def get_by_id(_id):
		pass

	# get equity by id 
	def get_by_equity_id(_id):
		pass

	# get all equity
	def get_all():
		pass

	# get all equity
	def stocks_balance(_user_id):
		stock_balances = db.session.query(EquityStock).filter_by(user_id=_user_id).all()
		return [EquityStock.json(stock) for stock in stock_balances]



