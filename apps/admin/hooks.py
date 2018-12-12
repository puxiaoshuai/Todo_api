from .views import admin
import config
from flask import render_template
from .models import *


@admin.errorhandler(404)
def page_not_found(e):
    return render_template('base/page_404.html'), 404
