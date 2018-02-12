import tweepy

retweeter_tree = []


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


'''
def get_root_connection_list(api, ruser, root_retweeters_data_list):
    # ツイート主のフォロワーを取得(RTDataのリスト)
    followers_id_list = get_follower_ids(api, ruser.user_id)

    # rootユーザをフォロー&ツイートをRTしたユーザのリストを取得(RTData型)
    return get_retweeter_data(root_retweeters_data_list, followers_id_list)
'''


def trace_tree(api, retweeters_data_list, root_retweeters_data_list):
    for rdata in retweeters_data_list:
        # フォロワーのidを取得
        followers_id_list = get_follower_ids(api, rdata.user_id)

        # ユーザをフォロー&ツイートをRTしたユーザのリストを取得(RTData型)
        retweeters_data_list2 = get_retweeter_data(root_retweeters_data_list, followers_id_list)

        # つながりを設定
        if len(retweeters_data_list2) != 0:
            set_connection(rdata, retweeters_data_list2)
            trace_tree(api, retweeters_data_list2, root_retweeters_data_list)


def analyze_main(api, ruser, root_retweeters_data_list):
    # rootユーザをフォロー&ツイートをRTしたユーザのリストを取得(RTData型)
    # retweeters_data_list = get_root_connection_list(api, ruser, root_retweeters_data_list)

    # つながりを設定
    # set_connection(ruser, retweeters_data_list)

    # 再帰的に繋がりを探していく
    retweeters_data_list = [ruser]
    trace_tree(api, retweeters_data_list, root_retweeters_data_list)
    return retweeter_tree
