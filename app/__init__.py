from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta

app = Flask(__name__)



from app.config import Config


db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_object(Config)
from app import models, routes, controllers
from app import errors

app.secret_key = 'secret key'


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


