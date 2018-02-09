import RTData


def get_rt_ids(api, sid):
    group_id = 0
    retweeter = api.retweets(sid, 100)  # RTしたユーザを取得(100件)
    retweeter_data = []  # RTData格納用

    for rter in retweeter:
        retweeter_data.append(RTData.RTData(rter.user.id, sid, rter.user.name, 1, group_id))  # 情報を抽出してRTData型として管理
        group_id += 1
        # user_idを基に他の情報を調べる手法だと応答にかなり時間がかかるため、つながりデータは後回しにしてRTDataを生成した。

    return retweeter_data


