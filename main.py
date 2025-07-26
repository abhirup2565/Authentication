from flask import Flask,jsonify
from extensions import db,jwt
from dotenv import load_dotenv
from auth import auth_blueprint
from users import user_blueprint
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
    app.register_blueprint(user_blueprint)


    #jwt error handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({"message":"Token is expired","error":"Token expired"}),401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed","error":"invalid token"}),401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"Request does not contain valid token","error":"authorization_header"}),401


    return app


app=create_app()

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run()
