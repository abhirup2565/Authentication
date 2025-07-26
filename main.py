from flask import Flask
from extensions import db,jwt
from dotenv import load_dotenv
from auth import auth_blueprint
load_dotenv()

def create_app():
    app=Flask(__name__)
    #config file
    app.config.from_prefixed_env()
    #initialising extentions
    db.init_app(app)
    jwt.init_app(app)
    #intialising blueprint
    app.register_blueprint(auth_blueprint)

    return app


app=create_app()

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run()
