import GetAndAnalyzeRTMain


def vr_main():
    print("ツイートのURLを入力してください")
    url = input(">>")
    GetAndAnalyzeRTMain.gaa_main(url)  # RTの取得・分析・登録


if __name__ == '__main__':
    vr_main()
