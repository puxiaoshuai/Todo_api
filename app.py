from flask import Flask
import config
from exts import db
from flask_migrate import Migrate
from flask_login import LoginManager
from apps.admin import admin
from apps.front import front
from  apps.app_v1 import app_v1


def regigter_blueprints(app):
    app.register_blueprint(admin)
    app.register_blueprint(front)
    app.register_blueprint(app_v1)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.configs.get(config_name))
    db.init_app(app)
    Migrate(db=db, app=app)
    regigter_blueprints(app)
    return app


app = create_app("development")
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1212,debug=True)
