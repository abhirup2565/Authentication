from app import create_app
from app.extensions import db,scheduler
from app.cron import scheduledTask

app=create_app()

if __name__=="__main__":
    with app.app_context():
        scheduler.add_job(id = 'Scheduled Task', func=scheduledTask, trigger="cron", hour=0)
        scheduler.start()
        db.create_all()
    app.run(debug=True)





