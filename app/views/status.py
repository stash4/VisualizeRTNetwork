from flask import Blueprint, render_template, request, flash
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
    ret = res.json()
    ret['id'] = tweet_id
    return ret


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


@status.route('/new', methods=['POST', 'GET'])
def add_tweet():
    '''
    新規ツイート登録ページ
    '''
    if request.method == 'POST' and request.form['tweet-id']:
        tweet_id = request.form['tweet-id']
        flash(f'Tweet(id: {tweet_id}) is Added.')
    return render_template('new.html', title='Add New Tweet')


@status.route('/<id>')
def graph(id):
    '''
    グラフ表示ページ
    '''
    data = {}
    return render_template('graph.html', title='Graph', data=data)
