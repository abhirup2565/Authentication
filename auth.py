from flask import Blueprint,jsonify,request
from models import User

auth_blueprint=Blueprint('auth',__name__)

@auth_blueprint.route('/register',methods=['POST'])
def register_user():
    data=request.get_json()
    user=User.get_user_by_username(username=data.get('username'))
    if user is not None:
        return jsonify({'error':"user already exist"}),409
    new_user = User(
       username=data.get('username'),
       email=data.get('email'),
    )
    new_user.set_password(password=data.get('password'))
    new_user.save()
    return jsonify({'message':'user created'}),201
        
    
