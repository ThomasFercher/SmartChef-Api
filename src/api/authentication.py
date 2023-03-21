from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    decode_token,
)
from utils.limiter import limiter, blacklist
import service.db as db
import utils.utils as utils
import json
from app import blacklist

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per second")
def login():
    request_body: dict = request.get_json()

    email = request_body.get("email")
    password = request_body.get("password")

    user = db.findUser(email)

    if user == None:
        return "User not found", 404
    if not utils.check_password(password, user.password):
        return "Wrong password or email", 401

    jwtToken = create_access_token(identity=user.id)

    return jsonify({"access_token": jwtToken}), 200


# Sign up
@auth_bp.route("/signup", methods=["POST"])
@limiter.limit("5 per second")
def signup():
    request_body: dict = request.get_json()

    email = request_body.get("email")
    password = request_body.get("password")
    hashed_password = utils.encrypt_password(password)

    statusString = db.createUser(email, hashed_password)
    dict = {"message": statusString}

    return Response(json.dumps(dict), status=200, mimetype="application/json")


# logout
@auth_bp.route("/logout", methods=["DELETE"])
@limiter.limit("5 per second")
@jwt_required()
def logout():
    token = request.headers.get("Authorization").split(" ")[1]
    claims = decode_token(token)
    jti = claims["jti"]
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


