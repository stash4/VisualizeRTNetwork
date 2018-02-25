from flask import Blueprint, render_template
import requests
from ..models import db, Tweet

params = {
    "hide_thread": "true",
    "dnt": "true"
}


def oembed_tweet(tweet_id, params=params):
    '''
    埋め込みツイートのマークアップを取得
    '''
    params['url'] = f'https://twitter.com/user/status/{tweet_id}'
    url = 'https://publish.twitter.com/oembed'
    res = requests.get(url, params=params)
    ret = res.json()
    ret['id'] = tweet_id
    return ret


def tweet_id_list():
    tweets = db.session.query(Tweet).all()
    return [tw.id for tw in tweets]


status = Blueprint('status', __name__)


@status.route('/list')
def status_list():
    '''
    ツイート一覧ページ
    '''
    tweet_ids = tweet_id_list()
    oembed_tweets = []
    for tw_id in tweet_ids:
        oembed_tweets.append(oembed_tweet(tw_id))
    return render_template(
        'status_list.html',
        title='Tweets',
        tweets=oembed_tweets)


@status.route('/<id>')
def graph(id):
    '''
    グラフ表示ページ
    '''
    tweet = oembed_tweet(id)
    data = {}
    return render_template('graph.html', title='Graph', tweet=tweet, data=data)
