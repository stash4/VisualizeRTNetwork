import tweepy
import json
import ast
import collections
import datetime
import RTDataDAO

retweeter_tree = []
node_id = set()
stop_tree = False


def check_api_limit(api):
    print("API残り呼び出し回数：あと：" + str(api.rate_limit_status("followers")["resources"]["followers"]["/followers/ids"]["remaining"]) + "回")
    if api.rate_limit_status("followers")["resources"]["followers"]["/followers/ids"]["remaining"] == 0:
        print("API制限に引っかかりました(◞‸◟)")
        print("解除時刻" + str(datetime.datetime.fromtimestamp(api.rate_limit_status("followers")["resources"]["followers"]["/followers/ids"]["reset"])))


def get_follower_ids(api, user_id, stext, sid):
    global stop_tree
    retweeter_follower = api.get_user(user_id).followers_count  # スクリーンネームからツイート主の情報を取得
    call_api_count = 1
    while True:
        retweeter_follower = retweeter_follower - 5000
        if retweeter_follower <= 0:
            break
        call_api_count += 1

    if api.rate_limit_status("followers")["resources"]["followers"]["/followers/ids"]["remaining"] - call_api_count < 0:
        # 現時点での分析結果を登録しておく
        retweeter_tree_dict = create_dict(retweeter_tree, stext, sid)
        RTDataDAO.register(retweeter_tree_dict)

        print("API制限にかかるため約15分待機します。中断しますか？ \"はい\"->y \"いいえ\"->それ以外のキー")
        key = input(">>")
        if key == "y":
            stop_tree = True
            return []

    check_api_limit(api)  # API制限の回数や制限に引っかかった時の再開時間を教えてくれる
    followers_ids = tweepy.Cursor(api.followers_ids, user_id=user_id).pages()  # フォロワーのidを取得。一度に5000人まで取得できるらしい。15分15回
    followers_id_list = []

    # followers_idsはtweepy.cursor.CursorIterator型になってるのでlistに変換
    for followers_id in followers_ids:
        followers_id_list.append(followers_id)
    return followers_id_list[0]


def create_user_id_list(retweeters_data_list):
    retweeters_id_list = []
    for rdata in retweeters_data_list:
        retweeters_id_list.append(int(rdata.user_id))
    return retweeters_id_list


def get_retweeter_data(retweeters_data_list, followers_id_list):
    # RTした人のデータからuserIDだけのリストを生成
    retweeters_id_list = create_user_id_list(retweeters_data_list)

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


def set_connection(ruser, retweeters_data_list, is_connect):
    if is_connect:
        for rdata in retweeters_data_list:
            if rdata.distance != 1.5:
                ruser.connection_list.append([rdata.user_id, rdata.distance])
            else:
                ruser.connection_list.append([rdata.user_id, ruser.distance + 1])
        retweeter_tree.append(ruser)
    else:
        for rdata in retweeters_data_list:
            ruser.connection_list.append([rdata.user_id, rdata.distance])


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
    deleted_list = []
    for rlist in retweeters_data_list:
        deleted_list.append(rlist)
    for rdata in retweeters_data_list:
        if rdata.user_id in node_id:
            print("削除：" + str(rdata.user_name) + "(" + str(rdata.user_id) + ")")
            deleted_list.remove(rdata)
            node_id.add(rdata.user_id)
    return deleted_list


def trace_tree(api, retweeters_data_list, root_retweeters_data_list, tree, status_text, status_id):
    # RTリストからidを抽出
    for rdata in retweeters_data_list:
        if not (rdata.user_id in node_id):
            node_id.add(rdata.user_id)

    for rdata in retweeters_data_list:
        if stop_tree:
            break

        print("階層" + str(tree))
        # フォロワーのidを取得
        followers_id_list = get_follower_ids(api, rdata.user_id, status_text, status_id)
        if len(followers_id_list) == 0:
            break

        # ユーザをフォロー&ツイートをRTしたユーザのリストを取得(RTData型)
        retweeters_data_list2 = get_retweeter_data(root_retweeters_data_list, followers_id_list)
        print("対象ノード：" + str(rdata.user_name))
        if len(retweeters_data_list2) == 0:
            print("子ノード：無し")
        for rd in retweeters_data_list2:
            print("子ノード：" + rd.user_name)

        # つながりを設定
        print("親ノード削除前：" + str(len(retweeters_data_list2)))
        rdata.connection_list = []  # 親ノードのつながりが入ってるみたいなので一回初期化
        rdata.distance = tree-1  # 同様の理由でにdistanceに階層の値を代入
        set_connection(rdata, retweeters_data_list2, True)

        # 親ノードをRTリストから削除
        retweeters_data_list3 = check_upper_node(retweeters_data_list2)
        print("親ノード削除後：" + str(len(retweeters_data_list3)))

        # groupを設定
        retweeters_data_list4 = set_group(rdata, retweeters_data_list3)

        # 再帰呼び出し
        trace_tree(api, retweeters_data_list4, root_retweeters_data_list, tree+1, status_text, status_id)


def add_unconnected_user(ruser, rtree, rrd_list):
    new_tree = []
    for rrd in rrd_list:
        if rrd.user_id not in node_id:
            new_tree.append(rrd)

    set_connection(ruser, new_tree, False)

    for nt in new_tree:
        rtree.append(nt)
    return rtree


def create_dict(tree, stext, sid):
    # json風に変換
    data_str = "{"
    data_str += "\"tweetid\":" + str(sid) + ","
    data_str += "\"text\":\"\"\"" + stext + "\"\"\","
    data_str += "\"users\":["
    for trid in tree:
        data_str += "{\"userid\":" + str(trid.user_id) + ", \"name\":\"" + str(trid.user_name) + "\", \"group\":" + str(trid.group) + "},"
    data_str += "], \"links\":["
    for trlink in tree:
        for trcnt in trlink.connection_list:
            data_str += "{\"source\":" + str(trlink.user_id) + ", \"target\":" + str(trcnt[0]) + ", \"distance\":" + str(trcnt[1]) + "},"
    data_str += "]"
    data_str += "}"

    # dict型に変換してreturn
    dic = collections.OrderedDict(ast.literal_eval(data_str))

    # 途中で出力する場合は一部の情報を削除
    users_set = set()
    for item in dic["users"]:
        users_set.add(item["userid"])
    for item in dic["links"]:
        if not item["target"] in users_set:
            item["distance"] = -2
            item["source"] = 0
            item["target"] = 0

    print(json.dumps(dic, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))  # 整形したものを表示
    return dic


def analyze_main(api, ruser, root_retweeters_data_list, status_text):
    # 再帰的に繋がりを探していく
    retweeters_data_list = [ruser]
    trace_tree(api, retweeters_data_list, root_retweeters_data_list, 1, status_text, ruser.status_id)
    if not stop_tree:
        new_retweeter_tree = add_unconnected_user(ruser, retweeter_tree, root_retweeters_data_list)
        for rt in new_retweeter_tree:
            print(rt.user_name)
        return create_dict(new_retweeter_tree, status_text, ruser.status_id)
    else:
        return create_dict(retweeter_tree, status_text, ruser.status_id)
