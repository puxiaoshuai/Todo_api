from flask import (Blueprint, views, render_template, request, flash,abort,
                   session, redirect, url_for, g, jsonify)

front = Blueprint('front', __name__)


@front.route("/")
def index():
     return  render_template('front/index.html')
