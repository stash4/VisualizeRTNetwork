import os
from .RTData import RTData
from ..models import db, Tweet
import tweepy


def get_rt_data(api, sid):
    retweeter_data = []  # RTData格納用
    retweeter_id_set = set()

    tweet = db.session.query(Tweet).filter_by(id=sid).first()
    if tweet is not None:
        users = tweet.users
        for user in users:
            retweeter_id_set.add(user.id)
            retweeter_data.append(RTData(user.id, sid, user.name))

    retweeter = api.retweets(sid, 100)  # RTしたユーザを取得(100件)

    for rter in retweeter:
        if rter.user.id not in retweeter_id_set:
            retweeter_data.append(RTData(rter.user.id, sid, rter.user.name))  # 情報を抽出してRTData型として管理
            # user_idを基に他の情報を調べる手法だと応答にかなり時間がかかるため、つながりデータは後回しにしてRTDataを生成した。

    return retweeter_data


def set_api():
    # TwitterAPIの認証
    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'],
                               os.environ['CONSUMER_SECRET_KEY'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'],
                          os.environ['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True)  # 2つ目の引数はAPI制限に引っかかった時に待つかどうかを選ぶオプション
    return api


def get_root_user(api, status_id):
    tweet = api.get_status(status_id)  # IDからツイートの情報を取得
    tweeter = tweet.user
    tweeter_id = tweeter.id_str  # その中からuserIDを抜き出す
    tweeter_name = tweeter.name  # ユーザ名も抜き出す
    tweet_text = tweet.text  # 本文を取得
    root_user = RTData(tweeter_id, status_id, tweeter_name, 0, -1)  # RTData型で管理する
    return root_user, tweet_text
