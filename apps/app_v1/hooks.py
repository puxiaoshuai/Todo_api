from apps.app_v1.resources import app_v1
import config
from flask import session, g
from .models import User


@app_v1.before_request
def before_app_request():
    if config.USER_ID in session:
        user_id = session.get(config.USER_ID)
        user = User.query.get(user_id)
        if user:
            g.user = user
