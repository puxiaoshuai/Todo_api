from flask_restful import reqparse
from flask import g
from apps.app_v1.HttpBase import generate_response, ResponseCode


def check_token():
    parse = reqparse.RequestParser()
    parse.add_argument("token")
    token = parse.parse_args().get("token","0")
    print("客户端token"+token)
    user = g.user
    if user.verify_auth_token(token):
        print("验证token成功")
        return True
    else:
        print("验证token失败")
        return False

