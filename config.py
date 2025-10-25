from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS 
from dotenv import load_dotenv 

load_dotenv() 

app = Flask(__name__)

CORS(app , resources={r"/api/*" : { "origin" : "http://localhost:5173" }})

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True 

db = SQLAlchemy(app) 

