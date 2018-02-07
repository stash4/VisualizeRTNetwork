from flask import Blueprint, render_template

status = Blueprint('status', __name__)


@status.route('/list')
def status_list():
    ids = []

    return render_template('status_list.html', title='Tweets', ids=ids)


@status.route('/<id>')
def graph(id):
    data = {}
    return render_template('graph.html', title='Graph', data=data)
