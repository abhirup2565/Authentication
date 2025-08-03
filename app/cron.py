from flask_apscheduler import APScheduler

scheduler=APScheduler() 
 #CRON JOB
def scheduledTask():
    print("Testing app scheduler")