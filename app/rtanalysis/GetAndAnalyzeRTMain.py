import AnalyzeRTData
import GetRTConnection

''' ここの必要性が分からなくなってきた
def get_rt_data(give_api, sid):
    return GetRTConnection.get_rt_data(give_api, sid)


def analyze_rt(give_api, tid, rlist):
    AnalyzeRTData.get_user_data(give_api, tid, rlist)
'''


def gaa_main(url="https://twitter.com/jr_tduniv/status/877352450398732292"):  # 初期値はイタリアントマト
    # API認証
    api = GetRTConnection.set_api()
    # ツイート主の情報を取得
    root_user = GetRTConnection.get_root_user(api, url)
    # RTしたユーザの情報を取得(100件)
    retweeter_data_list = GetRTConnection.get_rt_data(api, root_user.status_id)

    # データ確認用
    '''
    for ist in retweeter_data_list:
        print("ユーザID：" + str(ist.user_id))
        print("リツイートしたツイートのID：" + str(ist.status_id))
        print("ユーザ名：" + ist.user_name)
        print("つながりリスト：" + str(ist.connection_list))
    '''

    # 取得した情報からつながりを分析してデータを返す
    return AnalyzeRTData.analyze_main(api, root_user, retweeter_data_list)


gaa_main()
