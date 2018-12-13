from functools import wraps
from flask import session, g,redirect,url_for
from config import USER_ID
from .models import User

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
