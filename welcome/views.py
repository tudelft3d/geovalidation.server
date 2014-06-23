from welcome import app

from flask import render_template, send_from_directory

@app.route("/")
def index():
    return render_template("index.html")
