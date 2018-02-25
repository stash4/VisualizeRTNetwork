from . import AnalyzeRTData, GetRTConnection, RTDataDAO

# https://twitter.com/TDU_webmaster/status/963293178307665920 サブ


def gaa_main(url="https://twitter.com/jr_tduniv/status/877352450398732292"):  # 初期値はイタリアントマト
    # API認証
    api = GetRTConnection.set_api()
    # ツイート主の情報を取得
    root_user, status_text = GetRTConnection.get_root_user(api, url)
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

    # 取得した情報からつながりを分析してデータを返す(dict型)
    retweeter_tree_dict = AnalyzeRTData.analyze_main(api, root_user, retweeter_data_list, status_text)

    """
    dict型データの取り出し例
    "tweetid" -> retweeter_tree_dict["tweetid"]
    "text" -> retweeter_tree_dict["text"]
    "links" -> retweeter_tree_dict["links"]
        "distance" -> 
            for item in retweeter_tree_dict["links"]:
                item["distance"]
        "source" -> 
            for item in retweeter_tree_dict["links"]:
                item["source"]
        "target" -> 
            for item in retweeter_tree_dict["links"]:
                item["target"]
    "users" -> retweeter_tree_dict["users"]
        "group" -> 
            for item in retweeter_tree_dict["users"]:
                item["group"]
        "name" -> 
            for item in retweeter_tree_dict["users"]:
                item["name"]
        "userid" -> 
            for item in retweeter_tree_dict["users"]:
                item["userid"]
    """

    # データベースに登録
    RTDataDAO.register(retweeter_tree_dict)


if __name__ == '__main__':
    gaa_main()
