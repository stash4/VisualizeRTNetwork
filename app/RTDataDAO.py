from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////magical.db'
db = SQLAlchemy(app)


class Tweets(db.Model):
    __tweet_info__= 'tweets'
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text)

    def __int__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        return f'<Tweet id={self.id} text={self.text}>'

class User(db.Model):
    __user_info__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Name)

    def __int__(self, id, name):
       self.id = id
       self.name = name

    def __repr__(self):
       return f'<User id={self.id} name={self.name}>'

class Connection(db.Model):
   __connection_tweets__ = 'connection'
   target_ids = db.Coulmn(db.Integer,db.Integer)
   group = db.Coulmn(db.Integer)
   value = db.Coulmn(db.Integer)

   def __int__(self, tid, uid, target_ids, group, value):
       self.tid = Tweets.id
       self.uid = User.id
       self.target_ids = target_ids
       self.group = group
       self.value = value

   def __repr__(self):
       return f'<Connection tid={Tweets.id} uid={User.id}' \
              f'target={self.target_ids} group={self.group}' \
              f'value={self.value}>'


def register(retweeter_tree):
    db.session.add()
    db.session.commit()
