import uuid
from app import db


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Text, primary_key=True)
    text = db.Column(db.Text)
    users = db.relationship('User', backref='tweets', lazy=True)
    links = db.relationship('Link', backref='tweets', lazy=True)

    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        return f'<Tweet id={self.id} text=\"{self.text}\">'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text, primary_key=True)
    tweet_id = db.Column(db.Text, db.ForeignKey('tweets.id'),
                         primary_key=True)
    name = db.Column(db.Text)
    group = db.Column(db.Integer)

    def __init__(self, id, tweet_id, name, group):
        self.id = id
        self.tweet_id = tweet_id
        self.name = name
        self.group = group

    def __repr__(self):
        return f'<User id={self.id} tweet_id={self.tweet_id} '\
            f'name=\"{self.name}\" group={self.group}>'


class Link(db.Model):
    __tablename__ = 'links'
    uuid = db.Column(db.Text, primary_key=True)
    tweet_id = db.Column(db.Text, db.ForeignKey('tweets.id'))

    source_id = db.Column(db.Text)
    target_id = db.Column(db.Text)

    distance = db.Column(db.Integer)

    def __init__(self, tweet_id, source_id, target_id, distance):
        self.uuid = str(uuid.uuid4())
        self.tweet_id = tweet_id
        self.source_id = source_id
        self.target_id = target_id
        self.distance = distance

    def __repr__(self):
        return f'<Link uuid=\"{self.uuid}\" tweet_id={self.tweet_id} '\
            f'source_id={self.source_id} target_id={self.target_id} '\
            f'distance={self.distance}>'


def init():
    db.create_all()
