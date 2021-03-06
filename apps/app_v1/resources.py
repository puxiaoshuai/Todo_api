from flask import (Blueprint, views, render_template, request, flash, abort, make_response,
                   session, redirect, url_for, g, jsonify)
from flask_restful import Resource, abort, reqparse, Api
from apps.app_v1.models import User, TaskModel
from apps.app_v1.HttpBase import generate_response, ResponseCode
from exts import db
import qiniu
import os
import config
from apps.app_v1.decorators import login_required, check_app_token

app_v1 = Blueprint('todo', __name__, url_prefix='/todo/api')
api = Api(app=app_v1)


@app_v1.route("/uptoken/", methods=["POST"])
def up_token():
    access_key = "BkaslCENSa-EbKEjHbCExMprdB8FwTELgI_zOVZ5"  #5
    secret_key = 'GQbM6Y9Orc09bW6CyRn8qaLVmqoTCYo84iex1zUk'
    q = qiniu.Auth(access_key, secret_key)
    bucket = 'todo'
    # expires设置缓存时间15天,可自己设置
    token = q.upload_token(bucket=bucket, expires=3600 * 24 * 15)
    return jsonify(generate_response(data=token))


class TaskListView(Resource):
    decorators = [login_required, check_app_token]

    # 如果前端要访问，需要传token，过来做比较,True做其他操作
    def post(self):
        userid=session.get(config.USER_ID)
        parse = reqparse.RequestParser()
        parse.add_argument("page_size", type=str, default=config.PAGE_SIZE)
        parse.add_argument("page", required=True, type=str, help="page没有传递")
        page_size = parse.parse_args().get("page_size")
        page_index = parse.parse_args().get("page")
        total_num = len(TaskModel.query.filter_by(user_id=userid).order_by(TaskModel.create_time.desc()).all())

        tasks = TaskModel.query.filter_by(user_id=userid).order_by(TaskModel.create_time.desc()).limit(page_size).offset(
            (int(page_index) - 1) * int(page_size))
        task_list = [task.to_json() for task in tasks]
        to_data = {
            "page": page_index,
            'page_size': page_size
            , 'total_num': total_num,
            'list': task_list
        }
        return generate_response(data=to_data)


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
        parse.add_argument("files", action='append')
        id = parse.parse_args().get('id', "0")
        files = parse.parse_args().get("files", None)
        title = parse.parse_args().get('title')
        print(title)
        content = parse.parse_args().get('content')
        task = TaskModel.query.filter_by(id=id).first()
        if task:
            task.title = title
            task.content = content
            task.images=None if files is None else ",".join(files)
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
        parse.add_argument("files",action='append')
        title = parse.parse_args().get("title")
        content = parse.parse_args().get("content")
        files = parse.parse_args().get("files",None)
        print(files)
        user = g.user
        try:
            task = TaskModel(title=title, content=content, images=None if files is None else ",".join(files))
            task.user_id = user.id
            db.session.add(task)
            db.session.commit()
            return generate_response()
        except Exception as e:
            print(e.args)
            db.session.rollback()
            return generate_response(code=ResponseCode.CODE_SERVER_ERROE)


# 在客户端其实不用请求退出登录，这样子，电脑，移动端都能多端登录，因为都有存在的seesion
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
                return generate_response(message="登录成功", data=user.to_json())
            else:
                return generate_response(message="账号或者密码错误", code=ResponseCode.CODE_MESSAGE_ERROR)
        else:
            return generate_response(message="该账号没注册", code=ResponseCode.CODE_NOTFOUND)


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
