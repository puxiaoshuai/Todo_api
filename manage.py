# 该文件主要创建测试命令等
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.app_v1 import models as Task_Model
from exts import db
from app import create_app
app = create_app("development")
manage = Manager(app=app)
Migrate(app=app, db=db)
manage.add_command("db", MigrateCommand)
# python manage.py db migrate  迁移
# python manage.py db upgrade 映射到数据库
if __name__ == '__main__':
    manage.run()

"""
传参的
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
@manage.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):

"""
"""
不传参
@manage.command
def create_role():
"""

