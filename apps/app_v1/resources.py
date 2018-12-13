from flask import (Blueprint, views, render_template, request, flash, abort, make_response,
                   session, redirect, url_for, g, jsonify)
from flask_restful import Resource, abort, reqparse, Api
from apps.app_v1.models import User, TaskModel
from apps.app_v1.HttpBase import generate_response, ResponseCode
from exts import db
from apps.app_v1.utils import check_token
from config import USER_ID
from apps.app_v1.decorators import login_required

app_v1 = Blueprint('todo', __name__, url_prefix='/todo/api')
api = Api(app=app_v1)


# @app_v1.route("/tasks/",methods=["POST"])
# @login_required

class TaskListView(Resource):
    decorators = [login_required]

    # 如果前端要访问，需要传token，过来做比较,True做其他操作
    def post(self):
        if check_token():
            return "获取成功"
        else:
            return generate_response(code=ResponseCode.CODE_NOT_LOGIN, message="登录token失效")


class LogoutView(Resource):
    decorators = [login_required]

    def post(self):
        del session[USER_ID]
        return generate_response(message="注销成功")


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
                session[USER_ID] = user.id
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


# class Fail(Resource):
#
#     def get(self):
#         del session[USER_ID]
#         return generate_response(message="注销成功")

api.add_resource(LoginView, '/login/', endpoint='login')
api.add_resource(LogoutView, '/logout/', endpoint='logout')
api.add_resource(ResisterView, '/register/', endpoint='register')
api.add_resource(TaskListView, '/tasks/', endpoint='tasks')
