from ..models import db, Tweet, User, Link


def register_tweet(tweet_id, text):
    tweet = db.session.query(Tweet).filter_by(id=tweet_id).first()
    if tweet is None:
        tweet = Tweet(tweet_id, text)
        db.session.add(tweet)
        db.session.commit()
    return tweet


def init_user(user_id, tweet_id, name, group):
    user = db.session.query(User)\
             .filter_by(id=user_id, tweet_id=tweet_id).first()
    if user is None:
        user = User(user_id, tweet_id, name, group)
    return user


def init_link(tweet_id, source_id, target_id, distance):
    link = db.session.query(Link)\
             .filter_by(tweet_id=tweet_id, source_id=source_id,
                        target_id=target_id).first()
    if link is None:
        link = Link(tweet_id, source_id, target_id, distance)
    return link


def register(rt_tree_dict):
    tw_id = str(rt_tree_dict['tweetid'])
    tweet = register_tweet(tw_id, rt_tree_dict['text'])

    users = []
    for item in rt_tree_dict['users']:
        user = init_user(str(item['userid']), tw_id,
                         item['name'], item['group'])
        users.append(user)

    links = []
    for item in rt_tree_dict['links']:
        source = str(item['source'])
        target = str(item['target'])
        if source == '' and target == '':
            continue
        link = init_link(tw_id, source, target, item['distance'])
        links.append(link)

    tweet.users = users
    tweet.links = links
    db.session.commit()
