import tweepy


def trace_tree(retweeters_id_list): # ここで再帰処理を行う(予定)
    # retweeters_id_list = []
    for rid in retweeters_id_list:
        followers_ids = tweepy.Cursor(api.followers_ids, user_id=rid).pages()
        followers_id_list = []

        for followers_id in followers_ids:
            followers_id_list.append(followers_id)
        print(len(followers_id_list))
        print(followers_id_list[0])
        followers_id_list2 = followers_id_list[0]

        fler_set = set(followers_id_list2)  # set化
        retweeters_id_list = list(rter_set & fler_set)  # 2つのsetの論理積を取って共通の値を取得
        for mlist in matched_list:
            print(mlist)
    print(str(stage) + "段階目終了")
    stage += 1
    # if len(matched_list) == 0:


def set_connection(ruser, retweeters_id_list):
    for rlist in retweeters_id_list:
        if rlist.distance != -1:
            ruser.connection_list.append([rlist.user_id, ruser.distance + rlist.distance])
        else:
            ruser.connection_list.append([rlist.user_id, ruser.distance + 1])

    # データ確認用
    '''
    for rcnctn in ruser.connection_list:
        print(rcnctn)
    '''


def get_user_data(api, ruser, retweeters_data_list):
    # フォロワーのidを取得。一度に5000人まで取得できるらしい。15分15回
    followers_ids = tweepy.Cursor(api.followers_ids, user_id=ruser.user_id).pages()

    # followers_idsはtweepy.cursor.CursorIterator型になってるのでlistに変換
    followers_id_list = []
    for followers_id in followers_ids:
        followers_id_list.append(followers_id)
    followers_id_list2 = followers_id_list[0]

    # RTした人のデータからuserIDだけのリストを生成(ここ冗長)
    retweeters_id_list = []
    for rlist in retweeters_data_list:
        retweeters_id_list.append(int(rlist.user_id))

    # フォロワーの中でRTした人を取得
    rter_set = set(retweeters_id_list)  # set化
    fler_set = set(followers_id_list2)  # set化
    matched_list = list(rter_set & fler_set)  # 2つのsetの論理積を取って共通の値を取得
    for mlist in matched_list:
        print(mlist)  # ツイート主のフォロワーで且つRTした人だけを出力
    print("----------")

    # RTData型に戻す
    retweeters_data_list2 = []
    for mlist in matched_list:
        for rdlist in retweeters_data_list:
            if mlist == rdlist.user_id:
                retweeters_data_list2.append(rdlist)

    # データ確認用
    '''
    for rd2list in retweeters_data_list2:
        print(rd2list.user_id)
        print(rd2list.user_name)
    '''

    # つながりを設定
    set_connection(ruser, retweeters_data_list2)

    # RTした人から同様の処理で再帰的に繋がりを探していく
    # trace_tree(retweeters_data_list2)



