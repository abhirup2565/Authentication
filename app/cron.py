from .models import TokenBlockList
from .extensions import db,scheduler

 #CRON JOB
def scheduledTask():
    try:
            db.session.query(TokenBlockList).delete()
            db.session.commit()
            print("executed cron job")
    except Exception as e:
        print("could not execute cron job ",e)
    