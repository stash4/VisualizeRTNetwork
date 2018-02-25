import os
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from models import Tweet
from rtanalysis.RTDataDAO import db, register


def db_job():
    tweets = db.session.query(Tweet).all()
    for tw in tweets:
        if not tw.user and not tw.links:
            register(tw.id)


scheduler = BlockingScheduler(standalone=True, coalesce=True)
minutes = os.environ['INTERVAL_MINUTES']
scheduler.add_job(func=db_job, trigger=IntervalTrigger(minutes=minutes),
                  id='job1', replace_existing=False)
scheduler.start()
