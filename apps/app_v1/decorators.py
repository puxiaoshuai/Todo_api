from functools import wraps
from flask import session, g, redirect, url_for
from flask_restful import reqparse

from config import USER_ID


from apps.app_v1.HttpBase import generate_response, ResponseCode


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get(USER_ID):
            return func(*args, *kwargs)
        else:
            # 返回401，前端检测到401进行登录操作
            print("login_required")
            return generate_response(code=ResponseCode.CODE_NOT_LOGIN)

    return inner


def check_app_token(func):
    @wraps(func)
    def inner(*args, **kwargs):
        parse = reqparse.RequestParser()
        parse.add_argument("token")
        token = parse.parse_args().get("token", "0")
        try:
            user = g.user
            if user.verify_auth_token(token):
                return func(*args, *kwargs)
            else:
                return generate_response(message="登录token失效啦1,请重新登录", code=ResponseCode.CODE_NOT_LOGIN)
        except Exception as err:
            print(err.args)
            return generate_response(message="登录token异常,请重新登录", code=ResponseCode.CODE_NOT_LOGIN)

    return inner
