class ResponseCode:
    CODE_SUCCESS = 200  # 凡是成功都用
    CODE_HAS_RESOURCE = 202  # 资源存在了
    CODE_MESSAGE_ERROR = 203  # 提交的信息有误
    CODE_NO_PARAM = 400  # 参数错误
    CODE_NOT_LOGIN = 401  # 未认证
    CODE_NOTFOUND = 404  # 资源不存在
    CODE_SERVER_ERROE = 500  # 服务器错误

    msg = {
        CODE_SUCCESS: "成功",
        CODE_HAS_RESOURCE: "资源已存在",
        CODE_NO_PARAM: "参数错误",
        CODE_NOT_LOGIN: "没有登录",
        CODE_NOTFOUND: "找不到资源",
        CODE_SERVER_ERROE: "对不起，服务器错误",
        CODE_MESSAGE_ERROR:"信息有误"

    }


def generate_response(data=None,message=None, code=ResponseCode.CODE_SUCCESS):
    return {
        'message':message if message is not None else ResponseCode.msg.get(code, ResponseCode.msg[ResponseCode.CODE_SERVER_ERROE]),
        'code': code,
        'data': data
    }
