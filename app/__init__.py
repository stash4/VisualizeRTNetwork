from flask import Flask
from .views.status import status


def init_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.register_blueprint(status, url_prefix='/status')

    return app
