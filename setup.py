"""
This module initializes a Flask application with SQLAlchemy for database management
and Flask-Migrate for database migrations.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import config

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config.from_object(config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
