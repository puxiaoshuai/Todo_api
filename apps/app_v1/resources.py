from flask import (Blueprint, views, render_template, request, flash, abort, make_response,
                   session, redirect, url_for, g, jsonify)
from flask_restful import Resource, abort, reqparse, Api
from apps.app_v1.models import User, TaskModel
from apps.app_v1.HttpBase import generate_response, ResponseCode
from exts import db
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app_v1 = Blueprint('todo', __name__, url_prefix='/todo/api')
api = Api(app=app_v1)


@app_v1.route("/tasks/")
def index():
    return jsonify({"python": "111"})


@app_v1.route("/token/", methods=["GET"])
@auth.login_required
def get_auth_token():
    # 登录的时候，存储g.user,此处就能引用
    token = g.user.get_auth_token()
    return generate_response(data=token)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    print("=====")
    print(user)
    if not user or not user.check_pwd(password):
        return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify(generate_response(code=ResponseCode.CODE_NOT_LOGIN)), 401)


class LoginView(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("username", type=str, required=True)
        parse.add_argument("password", type=str, required=True)
        username = parse.parse_args().get("username")
        pwd = parse.parse_args().get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_pwd(pwd):
                g.user = user
                return generate_response(message="登录成功", data=user.to_json())
        else:
            return generate_response(message="该账号没注册")


class ResisterView(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("username", type=str, required=True)
        parse.add_argument("password", type=str, required=True)
        username = parse.parse_args().get("username")
        pwd = parse.parse_args().get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            return generate_response(data={}, code=ResponseCode.CODE_HAS_RESOURCE)
        else:
            try:
                user = User(username=username, password=pwd)
                db.session.add(user)
                db.session.commit()
                return generate_response(data={})
            except:
                print("存储失败")
                db.session.rollback()


api.add_resource(LoginView, '/login/', endpoint='login')
api.add_resource(ResisterView, '/resister/', endpoint='register')
