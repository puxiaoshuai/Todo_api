from flask import (Blueprint, views, render_template, request, flash, abort, make_response,
                   session, redirect, url_for, g, jsonify)
from flask_restful import Resource, abort, reqparse, Api
from apps.app_v1.models import User, TaskModel
from apps.app_v1.HttpBase import generate_response, ResponseCode
from exts import db

import config
from apps.app_v1.decorators import login_required, check_app_token

app_v1 = Blueprint('todo', __name__, url_prefix='/todo/api')
api = Api(app=app_v1)


@app_v1.route("/")
def index():
    return "测试机"

class TaskListView(Resource):
    decorators = [login_required, check_app_token]

    # 如果前端要访问，需要传token，过来做比较,True做其他操作
    def post(self):
        tasks = TaskModel.query.all()
        print(tasks)
        task_list = [task.to_json() for task in tasks]
        return generate_response(data=task_list)


# 想想前台的删除，只是把状态改成了127，不存在真正的删除，前台收到200，自动把当前一条移动走就相当于删除成功啦
class TaskDelView(Resource):
    decorators = [login_required, check_app_token]

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("id", required=True)
        id = parse.parse_args().get('id', "0")
        task = TaskModel.query.filter_by(id=id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return generate_response(data=[])
        else:
            return generate_response(code=ResponseCode.CODE_NOTFOUND)


class TaskEditView(Resource):
    decorators = [login_required, check_app_token]

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("id", required=True)
        parse.add_argument("title", required=True)
        parse.add_argument("content", required=True)
        id = parse.parse_args().get('id', "0")
        title = parse.parse_args().get('title')
        content = parse.parse_args().get('content')
        task = TaskModel.query.filter_by(id=id).first()
        if task:
            task.title = title
            task.content = content
            db.session.commit()
            return generate_response(message="编辑信息成功")
        else:
            return generate_response(code=ResponseCode.CODE_NOTFOUND)


class TaskAddView(Resource):
    decorators = [login_required, check_app_token]

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("title", required=True)
        parse.add_argument("content")
        title = parse.parse_args().get("title")
        content = parse.parse_args().get("content")
        user = g.user
        try:
            task = TaskModel(title=title, content=content)
            task.user_id = user.id
            db.session.add(task)
            db.session.commit()
            return generate_response()
        except:
            db.session.rollback()
            return generate_response(code=ResponseCode.CODE_SERVER_ERROE)


class LogoutView(Resource):

    def post(self):
        print("执行1")
        session.pop(config.USER_ID, None)
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

                session[config.USER_ID] = user.id
                print("session 存储成功")
                print(session.get(config.USER_ID))
                return generate_response(message="登录成功", data=user.to_json())
            else:
                return generate_response(message="账号或者密码错误",code=ResponseCode.CODE_MESSAGE_ERROR)
        else:
            return generate_response(message="该账号没注册",code=ResponseCode.CODE_NOTFOUND)


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


api.add_resource(TaskEditView, '/tasks/edit/', endpoint='task_edit')
api.add_resource(TaskDelView, '/tasks/del/', endpoint='task_del')
api.add_resource(TaskAddView, '/tasks/add/', endpoint='task_add')
api.add_resource(LoginView, '/login/', endpoint='login')
api.add_resource(LogoutView, '/logout/', endpoint='logout')
api.add_resource(ResisterView, '/register/', endpoint='register')
api.add_resource(TaskListView, '/tasks/', endpoint='tasks')
