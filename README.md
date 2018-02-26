# VisualizeRTNetwork

## Description
RTによるツイートの拡がり方を可視化する。

## Usage
1. requirements.txtからパッケージをインストール  
```
pip install -r requirements.txt
```
2. 環境変数を記述した `.env` を作成  
テンプレート: `.env.sample`  
  
3. 実行  
```
gunicorn app:app
```
データ取得用のスケジューラを実行
```
python -m app.worker.py
```
4. `http://127.0.0.1:5000/status/list` にアクセス  
ツイートを登録してしばらくするとグラフが表示されるようになる。
