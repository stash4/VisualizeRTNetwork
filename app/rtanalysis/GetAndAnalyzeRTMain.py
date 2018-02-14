import AnalyzeRTData
import GetRTConnection
# import RTDataDAO


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
    retweeter_tree = AnalyzeRTData.analyze_main(api, root_user, retweeter_data_list)

    # データ確認用
    print("--------------------分析結果出力--------------------")
    for rtree in retweeter_tree:
        print("[", end="")
        print("ユーザID：" + str(rtree.user_id) + ", ", end="")
        print("ユーザ名：" + rtree.user_name + ", ", end="")
        print("距離(階層)：" + str(rtree.distance) + ", ", end="")
        print("グループ：" + str(rtree.group) + ", ", end="")
        print("つながりリスト：", end="")
        for clist in rtree.connection_list:
            print(str(clist) + " ", end="")
        print("]")

    # データベースに登録
    # RTDataDAO.register(retweeter_tree)


gaa_main()
