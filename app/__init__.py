from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Initialize the app
app = Flask(__name__)

#login manager
login = LoginManager(app)

# Load the config file
app.config.from_object('config')

#sqlalchemy stuff
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

#load views and database models
from app import views, models

