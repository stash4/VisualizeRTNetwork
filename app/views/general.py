from flask import Blueprint, redirect

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return redirect('/status/list')
