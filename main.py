from flask import Flask
from extensions import db
from dotenv import load_dotenv
from models import User
load_dotenv()

def create_app():
    app=Flask(__name__)
    app.config.from_prefixed_env()
    db.init_app(app)
    return app


app=create_app()

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run()
