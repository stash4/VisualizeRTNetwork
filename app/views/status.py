from flask import Blueprint, render_template, redirect, request, flash, url_for
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
    ret = {}
    if res.status_code == 200:
        ret = res.json()
        ret['id'] = tweet_id
    return ret


def tweet_id_list():
    tweets = db.session.query(Tweet).all()
    return [tw.id for tw in tweets]


def rt_dict(tweet_id):
    tweet = db.session.query(Tweet).filter_by(id=tweet_id).first()
    if tweet is None:
        return {}

    rt_dict = {'tweetid': tweet.id, 'text': tweet.text}
    users = tweet.users
    links = tweet.links

    rt_dict['users'] = [{'userid': u.id, 'name': u.name, 'group': u.group}
                        for u in users]
    rt_dict['links'] = [{'source': l.source_id, 'target': l.target_id,
                         'distance': l.distance}
                        for l in links]
    return rt_dict


status = Blueprint('status', __name__)


@status.route('/list')
def status_list():
    '''
    ツイート一覧ページ
    '''
    tweet_ids = tweet_id_list()
    oembed_tweets = []
    for tw_id in tweet_ids:
        tw = oembed_tweet(tw_id)
        if tw:
            oembed_tweets.append(tw)

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
        oemb_tw = oembed_tweet(tweet_id)
        db_tw = db.session.query(Tweet).filter_by(id=tweet_id).first()
        rslt = ''
        if not oemb_tw:
            rslt = 'is unavailable.'
        elif db_tw:
            rslt = 'is already added.'
        else:
            db.session.add(Tweet(tweet_id, ''))
            db.session.commit()
            rslt = 'is added.'
        msg = f'Tweet(id: {tweet_id}) {rslt}'
        flash(msg)
    return render_template('new.html', title='Add New Tweet')


@status.route('/<id>')
def graph(id):
    '''
    グラフ表示ページ
    '''
    if id not in tweet_id_list():
        redirect(url_for('status_list'))
    tweet = oembed_tweet(id)
    data = rt_dict(id)
    return render_template('graph.html', title='Graph', tweet=tweet, data=data)
