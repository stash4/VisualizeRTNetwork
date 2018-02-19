from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views.status import status

app = Flask(__name__)
app.config.from_object('app.config')
app.register_blueprint(status, url_prefix='/status')

db = SQLAlchemy(app)
