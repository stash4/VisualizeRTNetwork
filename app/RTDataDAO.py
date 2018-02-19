from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import GetAndAnalyzeRTMain as Artmain
import GetRTConnection as rtcone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sampledb.sqlite3'
db = SQLAlchemy(app)

class Tweet_info(db.Model):#tweet情報を保存
    tweet = [rtcone.status_id]##,tweet内容]
    db.session().add_all(tweet)
    db.session().commit()


class User_info(db.Model):#user情報を保存
    user = [Artmain.rtree.user_id,Artmain.rtree.user_name]
    db.session().add_all(user)
    db.session().commit()

class Connection_tweet(db.Model):##繋がり情報を保存
    connnection = [Artmain.rtree.user_id,rtcone.status_id
        ,Artmain.ist.user_id,Artmain.rtree.distance]
    db.session().add_all(connnection)
    db.session().commit()