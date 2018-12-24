from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Srializer
from config import BaseConfig
import time


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(36), index=True)
    __password = db.Column(db.String(128))

    def __init__(self, password, username):
        self.password = password
        self.username = username
    def __repr__(self):
        return self.username
    # 返回加密的密码
    @property
    def password(self):
        return self.__password

    # 加密密码
    @password.setter
    def password(self, pwd):
        self.__password = generate_password_hash(pwd)

    # 检查密码
    def check_pwd(self, pwd):
        reslut = check_password_hash(self.password, pwd)
        return reslut

    def get_auth_token(self, expiration=600):
        # SECRET_KEY为秘钥
        s = Srializer(BaseConfig.SECRET_KEY, expires_in=expiration)
        #调用dumps把id值进行加密
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):

        s = Srializer(BaseConfig.SECRET_KEY)
        try:
            #进行loads解析
            data = s.loads(token)
            user = User.query.get(data['id'])
            return user
        except:
            print("user中token校验失败")
            return None

    def to_json(self):
        return {
            'username': self.username,
            # 以utf8编码对字符串str进行解码，获得字符串类型对象
            'token': self.get_auth_token().decode('utf-8')

        }


class TaskModel(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), index=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    images=db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref='task')

    @property
    def image_urls(self):
        return self.images.split(",")
    def __repr__(self):
        return "title is {}".format(self.title)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'create_time':self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
