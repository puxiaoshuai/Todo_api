from flask import (Blueprint, views, render_template, request, flash, abort,
                   session, redirect, url_for, g, jsonify)
import os

front = Blueprint('front', __name__)
base_dir = os.path.abspath(os.path.dirname(__file__))


@front.route('/update/', methods=["GET", "POST"])
def up_pic():
    if request.method == "POST":
        name = request.form["name"]
        try:
            file = request.files.get("files")
            path_static="D:\Python_project\Todo_api\static\img"
            up_path=os.path.join(path_static,file.filename)
            session['filename']="img/"+file.filename
            print("/img/"+file.filename)
            session['username']=name
            file.save(up_path)
        except:
            print("没传文件")

        return redirect(url_for('.up_pic'))
    else:
        filename=session.get("filename")
        username=session.get("username")
        data={
            'filename':filename,
            'username':username
        }
        return render_template("front/index.html",**data)
