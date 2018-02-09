import AnalyzeRTData
import GetRTConnection
import tweepy
import TwitterKey
import RTData


def get_rt_data(give_api, sid):
    return GetRTConnection.get_rt_ids(give_api, sid)


def analyze_rt(give_api, tid, rlist):
    AnalyzeRTData.get_user_data(give_api, tid, rlist)


def gaa_main(url="https://twitter.com/jr_tduniv/status/877352450398732292"):  # 初期値はイタリアントマト
    # TwitterAPIの認証作業
    auth = tweepy.OAuthHandler(TwitterKey.CONSUMER_KEY, TwitterKey.CONSUMER_SECRET_KEY)
    auth.set_access_token(TwitterKey.ACCESS_TOKEN, TwitterKey.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)  # 2つ目の引数はAPI制限に引っかかった時に待つかどうかを選ぶオプション

    # ツイートからツイートidとツイート主のuserIDを取得
    status_id = url.split("/")[5]  # ツイートID

    tweeter_screen_name = url.split("/")[3]  # スクリーンネーム
    tweeter_data = api.get_user(tweeter_screen_name)  # スクリーンネームからツイート主の情報を取得
    tweeter_id = tweeter_data.id  # その中からuserIDを抜き出す
    tweeter_name = tweeter_data.name  # ユーザ名も抜き出す
    root_user = RTData.RTData(tweeter_id, status_id, tweeter_name, 0)  # RTData型で管理する
    print(root_user.user_name)

    # RTしたユーザの情報を取得(100件)
    retweeter_data_list = get_rt_data(api, status_id)

    # データ確認用
    '''
    for ist in retweeter_data_list:
        print("ユーザID：" + str(ist.user_id))
        print("リツイートしたツイートのID：" + str(ist.status_id))
        print("ユーザ名：" + ist.user_name)
        print("つながりリスト：" + str(ist.connection_list))
    '''

    # 取得した情報からつながりを分析してデータを返す
    return analyze_rt(api, root_user, retweeter_data_list)


gaa_main()
