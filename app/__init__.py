from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.helpers.analysis import analysis

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://127.0.0.1/puc-ibm"
app.config['CORS_HEADERS'] = 'Content-Type'
mongo = PyMongo(app)