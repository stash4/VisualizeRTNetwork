from RTData import RTData
import tweepy
import TwitterKey


def get_rt_data(api, sid):
    retweeter = api.retweets(sid, 100)  # RTしたユーザを取得(100件)
    retweeter_data = []  # RTData格納用

    for rter in retweeter:
        retweeter_data.append(RTData(rter.user.id, sid, rter.user.name))  # 情報を抽出してRTData型として管理
        # user_idを基に他の情報を調べる手法だと応答にかなり時間がかかるため、つながりデータは後回しにしてRTDataを生成した。

    return retweeter_data


def set_api():
    # TwitterAPIの認証
    auth = tweepy.OAuthHandler(TwitterKey.CONSUMER_KEY, TwitterKey.CONSUMER_SECRET_KEY)
    auth.set_access_token(TwitterKey.ACCESS_TOKEN, TwitterKey.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)  # 2つ目の引数はAPI制限に引っかかった時に待つかどうかを選ぶオプション
    return api


def get_root_user(api, url):
    status_id = url.split("/")[5]  # ツイートID

    tweeter_screen_name = url.split("/")[3]  # スクリーンネーム
    tweeter_data = api.get_user(tweeter_screen_name)  # スクリーンネームからツイート主の情報を取得
    tweeter_id = tweeter_data.id  # その中からuserIDを抜き出す
    tweeter_name = tweeter_data.name  # ユーザ名も抜き出す
    tweeter_text = api.get_status(status_id).text  # 本文を取得
    root_user = RTData(tweeter_id, status_id, tweeter_name, 0, -1)  # RTData型で管理する
    return root_user, tweeter_text
