#### flask 项目基本框架目录搭建
###### apps下是前后台模块，可自行创建其他模块，每个模块下有自己的from验证，model文件，views为路由文件
###### spiders为爬虫获取数据
###### templates分为前，后台，公共部分，其他可自行增加

###### app.py  创建工厂函数，注册蓝图
###### config.py 文件配置，数据库配置等
###### exts.py 获取第三方，方便其他地方导入
###### manage.py 数据测试创建等，使用flask_scripts
###### 使用方式
"""git clone git@github.com:puxiaoshuai/BaseFlask.git
pip install -r requirements.txt
config中数据库自行配置，数据库名，密码，等
"""

###### 不同电脑办公，数据库迁移问题,直接 db upgrade
###### 开发问题记录
1. postman能获取tasklist,移动端传了token,却说是不能token失效
###### siper中爬取古诗数据
数据库设计的话，tags与古诗是多对多关系
经过排查是在浏览器会直接加载cookie，而客户端需要在网络请求中设置cookie，就好了。
###### api功能点,以及传递参数   "/logout/"; 
    "/login";(username,password)
    "/register/";(username,password)
    "/tasks/";(token,id)
    "/tasks/add/";(token)
    "/tasks/del/";(token,id)
    "/tasks/edit/";(token,id)
    
