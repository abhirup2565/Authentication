from app import create_app
from app.extensions import db
from app.cron import scheduler,scheduledTask

app=create_app()

if __name__=="__main__":
    scheduler.add_job(id = 'Scheduled Task', func=scheduledTask, trigger="interval", seconds=3)
    scheduler.start()
    with app.app_context():
        db.create_all()
    app.run(debug=True)





