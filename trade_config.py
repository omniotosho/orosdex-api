from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import app, db

# db = SQLAlchemy(app)

class TradeConfig(db.Model):
	
	# init trade configuration table
	__tablename__ = "trade_configurations"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime(), server_default=func.now())
	updated_at = db.Column(db.DateTime(), onupdate=func.now())

	# convert to json object
	def json(self):
		data = {
			"id": self.id,
			"name": self.name,
			"created_at": self.created_at,
			"updated_at": self.updated_at,
		}
		return data

	# represent data as Object
	def __repr__(self):
		data = {
			"id": self.id,
			"name": self.name,
			"created_at": self.created_at,
			"updated_at": self.updated_at,
		}
		return json.dumps(data)

	# fetch all trade configuration
	def fetch_all():
		trade_configs = db.session.query(TradeConfig).all()
		return [TradeConfig.json(config) for config in trade_configs]

	# fetch one trade configuration
	def fetch_one(_id):
		config = db.session.query(TradeConfig).filter_by(id=_id).first()
		return TradeConfig.json(config)

	# add configuration
	def add_new(_name):
		new_trade_config = TradeConfig(name=_name)
		db.session.add(new_trade_config)
		db.session.commit()
		return True

	# update trade configuration
	def update_config(_id, _name):
		trade_config = db.session.query(TradeConfig).filter_by(id=_id).first()
		trade_config.name = _name
		db.session.commit()
		return True

	# delete one trade configuration
	def delete_config(_id):
		trade_config = db.session.query(TradeConfig).filter_by(id=_id).delete()
		db.session.commit()
		return True