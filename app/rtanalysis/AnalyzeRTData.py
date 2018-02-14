import tweepy

retweeter_tree = []
node_id = set()


def get_follower_ids(api, user_id):
    followers_ids = tweepy.Cursor(api.followers_ids, user_id=user_id).pages()  # フォロワーのidを取得。一度に5000人まで取得できるらしい。15分15回
    followers_id_list = []

    # followers_idsはtweepy.cursor.CursorIterator型になってるのでlistに変換
    for followers_id in followers_ids:
        followers_id_list.append(followers_id)
    return followers_id_list[0]


def get_retweeter_data(retweeters_data_list, followers_id_list):
    # RTした人のデータからuserIDだけのリストを生成(ここ冗長)
    retweeters_id_list = []
    for rdata in retweeters_data_list:
        retweeters_id_list.append(int(rdata.user_id))

    # フォロワーの中でRTした人を取得
    fler_set = set(followers_id_list)  # set化
    rter_set = set(retweeters_id_list)  # set化
    matched_list = list(rter_set & fler_set)  # 2つのsetの論理積を取って共通の値を取得

    # RTData型に戻す
    retweeters_data_list2 = []
    for mid in matched_list:
        for rdata in retweeters_data_list:
            if mid == rdata.user_id:
                retweeters_data_list2.append(rdata)
    return retweeters_data_list2


def set_connection(ruser, retweeters_data_list):
    for rdata in retweeters_data_list:
        if rdata.distance != -1:
            ruser.connection_list.append([rdata.user_id, rdata.distance])
        else:
            ruser.connection_list.append([rdata.user_id, ruser.distance + 1])
    retweeter_tree.append(ruser)


def set_group(ruser, retweeter_data_list):
    group = 0
    for rdata in retweeter_data_list:
        if ruser.group == -1:
            rdata.group = group
            group += 1
        else:
            rdata.group = ruser.group
    return retweeter_data_list


def check_upper_node(retweeters_data_list):
    deleted_list = retweeters_data_list
    for rdata in retweeters_data_list:
        if rdata.user_id in node_id:
            deleted_list.remove(rdata)
    return deleted_list


def trace_tree(api, retweeters_data_list, root_retweeters_data_list, tree):
    # RTリストからidを抽出
    for rdata in retweeters_data_list:
        if not (rdata.user_id in node_id):
            node_id.add(rdata.user_id)

    for rdata in retweeters_data_list:
        print("階層" + str(tree))
        # フォロワーのidを取得
        followers_id_list = get_follower_ids(api, rdata.user_id)

        # ユーザをフォロー&ツイートをRTしたユーザのリストを取得(RTData型)
        retweeters_data_list2 = get_retweeter_data(root_retweeters_data_list, followers_id_list)
        if len(retweeters_data_list2) == 0:
            print("子ノード無し")
        for rd in retweeters_data_list2:
            print("子ノード：" + rd.user_name)

        # つながりを設定
        print("親ノード削除前：" + str(len(retweeters_data_list2)))
        rdata.connection_list = []  # 親ノードのつながりが入ってるみたいなので一回初期化
        rdata.distance = tree-1  # 同様の理由でにdistanceに階層の値を代入
        set_connection(rdata, retweeters_data_list2)

        # 親ノードをRTリストから削除
        retweeters_data_list3 = check_upper_node(retweeters_data_list2)
        print("親ノード削除後：" + str(len(retweeters_data_list3)))

        # groupを設定
        retweeters_data_list4 = set_group(rdata, retweeters_data_list3)

        # 再帰呼び出し
        trace_tree(api, retweeters_data_list4, root_retweeters_data_list, tree+1)


def analyze_main(api, ruser, root_retweeters_data_list):
    # 再帰的に繋がりを探していく
    retweeters_data_list = [ruser]
    node_id.add(ruser.user_id)
    trace_tree(api, retweeters_data_list, root_retweeters_data_list, 1)
    return retweeter_tree