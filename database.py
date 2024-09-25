from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
CORS(app)

# Upload folder
UPLOAD_FOLDER = 'excel'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/tridex'
app.config["SQLALCHEMY_DATABASE_URI"] = engine = f"sqlite:///{PROJECT_DIR}/se.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
# db.init_app(app)