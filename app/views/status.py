from flask import Blueprint, render_template
import requests

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
    return res.json()


status = Blueprint('status', __name__)


@status.route('/list')
def status_list():
    '''
    ツイート一覧ページ
    '''
    tweet_ids = []
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
    data = {}
    return render_template('graph.html', title='Graph', data=data)
