from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app

db = SQLAlchemy(app)

class Treasury(db.Model):
	
	# init users table
	__tablename__ = 'treasury_bills'
	id = db.Column(db.Integer, primary_key=True)
	security = db.Column(db.Text)
	market = db.Column(db.Text)
	sector = db.Column(db.Text)
	product_id = db.Column(db.Integer)
	description = db.Column(db.Text)
	maturity = db.Column(db.Text)
	closing_price = db.Column(db.Float(18, 2))
	discount_yield = db.Column(db.Float(18, 2))
	closing_date = db.Column(db.Text)
	next_close_date = db.Column(db.Text)
	closing_mkt_price = db.Column(db.Float(18, 2))
	prev_closing = db.Column(db.Float(18, 2))
	next_closing = db.Column(db.Float(18, 2))
	prev_closing_mkt_price = db.Column(db.Float(18, 2))
	next_closing_mkt_price = db.Column(db.Float(18, 2))
	EOM_mkt_price = db.Column(db.Float(18, 2))
	EOY_mkt_price = db.Column(db.Float(18, 2))
	EOM_date = db.Column(db.Text)
	EOY_date = db.Column(db.Text)
	prev_business_day = db.Column(db.Text)
	prev_trade_date = db.Column(db.Text)
	month_start_date = db.Column(db.Text)
	year_start_date = db.Column(db.Text)
	month_end_date = db.Column(db.Text)
	year_end_date = db.Column(db.Text)
	cost_of_funds = db.Column(db.Float(18, 2))
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# return Json
	def json(self):
		data = {
			'id': self.id,
			'security': self.security,
			'market': self.market,
			'sector': self.sector,
			'product_id': self.product_id,
			'description': self.description,
			'maturity': self.maturity,
			'closing_price': float(self.closing_price),
			'discount_yield': float(self.discount_yield),
			'closing_date': self.closing_date,
			'next_close_date': self.next_close_date,
			'closing_mkt_price': float(self.closing_mkt_price),
			'prev_closing': float(self.prev_closing),
			'next_closing': float(self.next_closing),
			'prev_closing_mkt_price': float(self.prev_closing_mkt_price),
			'next_closing_mkt_price': float(self.next_closing_mkt_price),
			'EOM_mkt_price': float(self.EOM_mkt_price),
			'EOY_mkt_price': float(self.EOY_mkt_price),
			'EOM_date': self.EOM_date,
			'EOY_date': self.EOY_date,
			'prev_business_day': self.prev_business_day,
			'prev_trade_date': self.prev_trade_date,
			'month_start_date': self.month_start_date,
			'year_start_date': self.year_start_date,
			'month_end_date': self.month_end_date,
			'year_end_date': self.year_end_date,
			'cost_of_funds': float(self.cost_of_funds),
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
			'product_id': self.product_id,
			'description': self.description,
			'maturity': self.maturity,
			'closing_price': float(self.closing_price),
			'discount_yield': float(self.discount_yield),
			'closing_date': self.closing_date,
			'next_close_date': self.next_close_date,
			'closing_mkt_price': float(self.closing_mkt_price),
			'prev_closing': float(self.prev_closing),
			'next_closing': float(self.next_closing),
			'prev_closing_mkt_price': float(self.prev_closing_mkt_price),
			'next_closing_mkt_price': float(self.next_closing_mkt_price),
			'EOM_mkt_price': float(self.EOM_mkt_price),
			'EOY_mkt_price': float(self.EOY_mkt_price),
			'EOM_date': self.EOM_date,
			'EOY_date': self.EOY_date,
			'prev_business_day': self.prev_business_day,
			'prev_trade_date': self.prev_trade_date,
			'month_start_date': self.month_start_date,
			'year_start_date': self.year_start_date,
			'month_end_date': self.month_end_date,
			'year_end_date': self.year_end_date,
			'cost_of_funds': float(self.cost_of_funds),
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}
		return json.dumps(data)

	# init add new
	def add_new(_security, _market, _sector, _product_id, _description, _maturity, _closing_price, _discount_yield, _closing_date, _next_close_date, _closing_mkt_price, _prev_closing, _next_closing, _prev_closing_mkt_price, _next_closing_mkt_price, _EOM_mkt_price, _EOY_mkt_price, _EOM_date, _EOY_date, _prev_business_day, _prev_trade_date, _month_start_date, _year_start_date, _month_end_date, _year_end_date, _cost_of_funds):
		# pass
		treasury_bill = db.session.query(Treasury).filter_by(security=_security).first()
		if(treasury_bill == None):
			new_treasury_bill = Treasury(security=_security, market=_market, sector=_sector, product_id=_product_id, description=_description, maturity=_maturity, closing_price=_closing_price, discount_yield=_discount_yield, closing_date=_closing_date, next_close_date=_next_close_date, closing_mkt_price=_closing_mkt_price, prev_closing=_prev_closing, next_closing=_next_closing, prev_closing_mkt_price=_prev_closing_mkt_price, next_closing_mkt_price=_next_closing_mkt_price, EOM_mkt_price=_EOM_mkt_price, EOY_mkt_price=_EOY_mkt_price, EOM_date=_EOM_date, EOY_date=_EOY_date, prev_business_day=_prev_business_day, prev_trade_date=_prev_trade_date, month_start_date=_month_start_date, year_start_date=_year_start_date, month_end_date=_month_end_date, year_end_date=_year_end_date, cost_of_funds=_cost_of_funds)
			db.session.add(new_treasury_bill)
			db.session.commit()

			# create new
			return {
				"status": "success",
				"message": _security + " added!"
			}
		else:
			# create new
			return {
				"status": "success",
				"message": _security + " already exist!"
			}

	# init add new
	def get_all():
		# pass
		treasury_bills = db.session.query(Treasury).all()
		return [Treasury.json(treasury) for treasury in treasury_bills]



