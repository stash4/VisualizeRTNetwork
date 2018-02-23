from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///magical.db'
db = SQLAlchemy(app)


class Tweet(db.Model):
    __table_name__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    def __init__(self, tid, text):
        self.id = tid
        self.text = text

    def __repr__(self):
        return f'<Tweet id={self.id} text={self.text}>'


class User(db.Model):
    __table_name__ = 'users'
    tweet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    group = db.Column(db.Integer)

    def __init__(self, tid, uid, name, group):
        self.tweet_id = tid
        self.user_id = uid
        self.name = name
        self.group = group

    def __repr__(self):
        return f'<User tweetid={self.tweet_id} userid={self.user_id} name={self.name} group={self.group}>'


class Connection(db.Model):
    _table_name__ = 'connection'
    tweet_id = db.Column(db.Integer)
    source_id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)

    def __init__(self, tid, source_id, target_id, distance):
        self.tweet_id = tid
        self.source_id = source_id
        self.target_id = target_id
        self.distance = distance

    def __repr__(self):
        return f'<Connection tid={self.tweet_id} ' \
               f'source={self.source_id} target={self.target_id} ' \
               f'value={self.distance}>'


def register(retweeter_tree_dict):
    db.create_all()
    tweet_id = retweeter_tree_dict["tweetid"]
    tweet = Tweet(tweet_id, retweeter_tree_dict["text"])
    if db.session.query(Tweet).filter_by(id=tweet_id).first() is None:
        db.session.add(tweet)
        db.session.commit()

    for item in retweeter_tree_dict["users"]:
        print(db.session.query(User).filter_by(tweet_id=tweet_id, user_id=item["userid"]).first())
        if db.session.query(User).filter_by(tweet_id=tweet_id, user_id=item["userid"]).first() is None:
            user = User(tweet_id, item["userid"], item["name"], item["group"])
            db.session.add(user)
            db.session.commit()

    for item in retweeter_tree_dict["links"]:
        print(db.session.query(Connection).filter_by(source_id=item["source"], target_id=item["target"]).first())
        if db.session.query(Connection).filter_by(source_id=item["source"], target_id=item["target"]).first() is None:
            if item["source"] == 0 and item["target"] == 0:
                continue
            connection = Connection(tweet_id, item["source"], item["target"], item["distance"])
            db.session.add(connection)
            db.session.commit()
    print("ok")
