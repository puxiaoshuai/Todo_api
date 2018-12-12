from flask import (Blueprint, views, render_template, request, flash,abort,
                   session, redirect, url_for, g, jsonify)

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route("/")
def index():
    return "首页"
