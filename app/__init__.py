from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app)

from .views.status import status
from .views.general import general
app.register_blueprint(status, url_prefix='/status')
app.register_blueprint(general, url_prefix='/')
