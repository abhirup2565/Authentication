from flask import Blueprint,jsonify,request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,get_jwt,
    current_user,
    get_jwt_identity)
from app.models import User,TokenBlockList

auth_blueprint=Blueprint('auth',__name__)


@auth_blueprint.route('/register',methods=['POST'])
def register_user():
    try:
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
    except Exception as e:
        return jsonify({'Something went wrong':e}),500


@auth_blueprint.route('/login',methods=["POST"])
def login():
    from datetime import timedelta
    data=request.get_json()
    user=User.get_user_by_username(username=data.get('username'))
    if user and user.check_password(password=data.get('password')):
        access_token=create_access_token(identity=user.username,expires_delta=timedelta(minutes=10))
        refresh_token=create_refresh_token(identity=user.username,expires_delta=timedelta(minutes=20) )
        print(access_token," and ",refresh_token)
        return jsonify({
                "Message":"logged in successfully",
                "tokens":{
                    "access":access_token,
                    "refresh":refresh_token
                }
        }),200
    return jsonify({"error":"invalid credential"}),400

@auth_blueprint.route('/who',methods=["GET"])
@jwt_required()
def who():
    return jsonify({"message":"Message about ","userdetail":{"username":current_user.username,"email":current_user.email}})

@auth_blueprint.route('/refresh',methods=["GET"])
@jwt_required(refresh=True)
def refresh_access():
    identity=get_jwt_identity()
    access_token=create_access_token(identity=identity)
    return jsonify({"New_Access_Token":access_token})

@auth_blueprint.route('/logout',methods=["GET"])
@jwt_required(verify_type=False)
def logout():
    jwt=get_jwt()
    jti=jwt['jti']
    token_type=jwt['type']
    token_block_list=TokenBlockList(jti=jti)
    token_block_list.save()
    return jsonify({"message":f"{token_type} is revoked successfully",}),200

@auth_blueprint.route('/blockList',methods=["GET"])
def view_blockList():
    from app.schemas import TokenBlockListSchema
    try:
        blockLists=TokenBlockList.query.all()
        result=TokenBlockListSchema().dump(blockLists,many=True)
        jti_list=[]
        for blockList in result:
            jti_list.append(blockList.get('jti'))
        return jsonify({"message":result},{"jti":jti_list})
    except Exception as e:
        return jsonify({"Something went wrong":str(e)})

@auth_blueprint.route('/deleteblockList',methods=["DELETE"])
def clear_blockList():
    from datetime import datetime,timedelta,timezone
    from app.models import TokenBlockList
    try:
        expiryTime = datetime.now(timezone.utc) - timedelta(minutes=10)
        expirytokens = TokenBlockList.query.filter(TokenBlockList.created_at < expiryTime).all()
        if expirytokens:
            for expirytoken in expirytokens:
                expirytoken.deleteBlockList()
            return jsonify({"message":"all expired token were deleted"})
        return jsonify({"message":"No expired token in db"})
    except Exception as e:
        return jsonify({"Something went wrong":str(e)})

        

