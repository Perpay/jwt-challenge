__author__ = 'arikmisler'
from flask import Flask, jsonify, request, make_response, current_app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from functools import update_wrapper
from flask_cors import CORS, cross_origin


from werkzeug.security import safe_str_cmp
import json
from datetime import *

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'you@perpay.com', 'password'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 'super-perpay-secret'
app.config['JWT_AUTH_ENDPOINT'] = '/v1/auth'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_AUTH_PASSWORD_KEY'] = 'password'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=1)


jwt = JWTManager(app)
CORS(app, resources=r'/v1/*')


@app.route('/v1/auth/', methods=['POST','OPTIONS'])
@cross_origin(allow_headers='*')
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('email', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    try:
        user = authenticate(username, password)
        if not user:
            return jsonify({"msg": "Invalid Credentials"}), 401
    except:
        return jsonify({"msg": "Invalid Credentials"}), 401




    # Identity can be any data that is json serializable
    ret = {
        'access': create_access_token(identity=username),
        'refresh': create_refresh_token(identity=username)
    }
    return jsonify(ret), 200

@app.route('/v1/auth-refresh/', methods=['POST','OPTIONS'])
@cross_origin(allow_headers='*')
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@app.route('/v1/transactions/', methods=['GET','OPTIONS'])
@cross_origin(allow_headers='*')
@jwt_required
def transactions():
    data = [{"type":"order", "amount": 1000, "id": 1 },
            {"type":"order", "amount": 500, "id": 12 },
            {"type":"deposit", "amount": 100, "id": 1102 }]
    return jsonify(data)

@app.route('/v1/credit_summaries/', methods=['GET','OPTIONS'])
@cross_origin(allow_headers='*')
@jwt_required
def credit_summaries():
    data = {
            "borrower_status": "good",
            "outstanding_task": None
            }
    return jsonify(data), 200

@app.route('/v1/power_breakdowns/', methods=['GET','OPTIONS'])
@cross_origin(allow_headers='*')
@jwt_required
def power_breakdowns():
    data = {"purchasing_power":690.0,"credit_limit":690.0,"available_credit":690.0,"cash_balance":0.0,
            "credits":{"highest_potential":0.0,"required_minimum":0.0,"expiring_soon":None}}
    return jsonify(data), 200




if __name__ == '__main__':
    app.run()