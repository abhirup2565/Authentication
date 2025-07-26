from flask import Flask
from extensions import db
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app=Flask(__name__)
    app.config.from_prefixed_env()
    db.__init__(app)
    return app


app=create_app()

if __name__=="__main__":
    with app.app_context():
        create_app()
    app.run()
