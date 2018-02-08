import GetAndAnalyzeRTMain


def get_rt_ids(api, sid):
    retweeter = api.retweets(sid, 100)  # RTしたユーザを取得(100件)
    retweeter_data = []  # RTData格納用

    for rter in retweeter:
        retweeter_data.append(GetAndAnalyzeRTMain.RTData(rter.user.id, sid, rter.user.name))  # 情報を抽出してRTData型として管理
        # user_idを基に他の情報を調べる手法だとかなり時間がかかるため、つながりデータは後回しにしてRTDataを生成した。

    return retweeter_data


