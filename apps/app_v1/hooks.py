from apps.app_v1.resources import app_v1
import config
from flask import session, g
from .models import User


@app_v1.before_request
def before_request():
    if session.get(config.USER_ID):
        user_id = session.get(config.USER_ID)
        print("每次请求前，获取的user_id {}".format(user_id))
        print("user_id is {}".format(user_id))
        user = User.query.get(user_id)
        print("user. {}".format(user))
        if user:
            g.user = user
    else:
        print("session 中没有 User_ID的键")
