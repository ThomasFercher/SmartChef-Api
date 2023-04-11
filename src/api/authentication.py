from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    decode_token,
    get_jwt_identity
)
from utils.limiter import  blacklist
import service.db as db
import utils.utils as utils
import json
from app import blacklist

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/test", methods=["Get"])
@jwt_required()
def test():
    return jsonify({"message": "test"}), 200
    

@auth_bp.route("/login", methods=["POST"])
def login():
    request_body: dict = request.get_json()

    email = request_body.get("email")
    password = request_body.get("password")

    user = db.findUser(email)

    if user == None:
        return Response(json.dumps({"msg":"User not found"}), 404,mimetype="application/json")
    if not utils.check_password(password, user.password):
        return Response(json.dumps({"msg":"Invalid Password or Email"}), 401,mimetype="application/json")

    jwtToken = create_access_token(identity=user.id)

    return jsonify({"access_token": jwtToken}), 200


# Sign up
@auth_bp.route("/signup", methods=["POST"])
def signup():
    request_body: dict = request.get_json()

    email = request_body.get("email")

    if db.findUser(email) != None:
        return Response(json.dumps({"msg":"User already exists"}), 400,mimetype="application/json")

    password = request_body.get("password")
    hashed_password = utils.encrypt_password(password)

    statusString = db.createUser(email, hashed_password)
    dict = {"msg": statusString}

    return Response(json.dumps(dict), status=200, mimetype="application/json")


# logout
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    token = request.headers.get("Authorization").split(" ")[1]
    claims = decode_token(token)
    jti = claims["jti"]
    blacklist.add(jti)
    return Response(json.dumps({"msg": "Successfully logged out"}), 200, mimetype="application/json")


# delete account
@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete():
    logout()

    id = get_jwt_identity()

    if not db.deleteUser(id): 
        return Response(json.dumps({"msg": "Error deleting Acount"}), 500, mimetype="application/json")
    
    return Response(json.dumps({"msg": "Successfully deleted Acount"}), 200, mimetype="application/json")


# getUser
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def getUser():
    id = get_jwt_identity()
    user = db.findUserById(id)
    if user == None:
        return "User not found", 404

    return Response(json.dumps(user.to_json()), 200, mimetype="application/json")
