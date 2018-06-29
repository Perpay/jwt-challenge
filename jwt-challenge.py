__author__ = 'arikmisler'
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import json

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'you@perpay.com', 'areallysecurepassword'),
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
app.config['SECRET_KEY'] = 'super-perpay-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/api/v1/transactions')
@jwt_required()
def protected():
    data = {[{"type":"order", "amount": 1000, "id": 1 },
            {"type":"order", "amount": 500, "id": 12 },
            {"type":"deposit", "amount": 100, "id": 1102 }]}
    return json.dumps(data)

@app.route('/api/v1//credit_summaries')
@jwt_required()
def protected():
    data = {
            "borrower_status": "good",
            "outstanding_task": None
            }
    return '%s' % current_identity

@app.route('/api/v1//power_breakdowns')
@jwt_required()
def protected():
    data = {"purchasing_power":690.0,"credit_limit":690.0,"available_credit":690.0,"cash_balance":0.0,
            "credits":{"highest_potential":0.0,"required_minimum":0.0,"expiring_soon":None}}
    return json.dumps(data)

if __name__ == '__main__':
    app.run()