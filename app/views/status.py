from flask import Blueprint, render_template
import requests

params = {
    "hide_thread": "true,"
    "dnt": "true"
}


def oembed_tweet(id, params=params):
    '''
    埋め込みツイートのマークアップを取得
    '''
    params['url'] = f'https://twitter.com/user/status/{id}'
    url = 'https://publish.twitter.com/oembed'
    res = requests.get(url, params=params)
    return res.json()['html']


status = Blueprint('status', __name__)


@status.route('/list')
def status_list():
    '''
    ツイート一覧ページ
    '''
    ids = []

    return render_template('status_list.html', title='Tweets', ids=ids)


@status.route('/<id>')
def graph(id):
    '''
    グラフ表示ページ
    '''
    data = {}
    return render_template('graph.html', title='Graph', data=data)
