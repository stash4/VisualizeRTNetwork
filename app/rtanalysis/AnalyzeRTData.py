import tweepy


def get_user_data(api, tid, retweeters_data_list):
    # フォロワーのidを取得。一度に5000人まで取得できるらしい。15分15回
    followers_ids = tweepy.Cursor(api.followers_ids, user_id=tid).pages()

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
    print("1段階目開始")
    rter_set = set(retweeters_id_list)  # set化
    fler_set = set(followers_id_list2)  # set化
    matched_list = list(rter_set & fler_set)  # 2つのsetの論理積を取って共通の値を取得
    for mlist in matched_list:
        print(mlist)  # ツイート主のフォロワーで且つRTした人だけを出力
    print("1段階目終了")

    # RTした人から同様の処理でさらに繋がりを探していく
    '''
    この処理が再帰的であることに気付いたところなので書き直す予定
    ちなみにこれだと動かない
    stage = 2
    while(True):
        print(str(stage) + "段階目開始")
        retweeters_id_list = []
        for rid in matched_list:
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
        if len(matched_list) == 0:
            break
    '''



