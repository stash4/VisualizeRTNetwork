from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app)

from .views.status import status
app.register_blueprint(status, url_prefix='/status')
