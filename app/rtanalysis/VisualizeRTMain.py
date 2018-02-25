import GetAndAnalyzeRTMain


def vr_main():
    print("ツイートのURLを入力してください")  # ここはコンソールで入力？
    url = input(">>")
    # urlのチェックはGetRTConnectionで行う(正しいURLかどうかをAPIで判断)

    '''
    # 当初はツイートを監視する予定だったのでツイートの取得数や取得時間を選ぶオプションがこの辺に来る。(進捗次第)    
    while True:
        print("ツイートの取得を切り上げる条件を選んでください。\"時刻\"->1 \"件数\"->2")
        conditions = input(">>")
        if conditions == 1 or conditions == 2:
            break
        else:
            print("不正な入力")

    if conditions == 1:
        print("取得時間を入力してください")
    else:
        print("取得件数を入力してください")

    number = input(">>")
    GetAndAnalyzeRTMain.gaa_main(url, conditions, number)  # RTの取得・分析・登録
    '''

    GetAndAnalyzeRTMain.gaa_main(url)  # RTの取得・分析・登録

    # 分析結果の表示をする処理


vr_main()
