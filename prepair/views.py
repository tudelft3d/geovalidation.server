from prepair import app
from settings import *

from flask import render_template, request, redirect, url_for
import os
import subprocess



@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")
    
@app.route('/faq')
def faq():
    return render_template("faq.html")


# def get_job_id():
#     return str(uuid.uuid4()).split('-')[0]

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template("index.html")




@app.route('/', methods=['GET', 'POST'])
def index():
    print "hugo"
    if request.method == 'POST':
        thewkt = request.form['thewkt']
        if thewkt == "":
            return render_template("index.html", problem="You must give a polygon's WKT")
        print thewkt
        cmd = []
        cmd.append(PREPAIREXE)
        cmd.append("--wkt ")
        cmd.append('POLYGON((0 0, 0 10, 10 0, 10 10, 0 0))')
        print cmd
        op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        R = op.poll()
        if R:
          res = op.communicate()
          raise ValueError(res[1])
        o =  op.communicate()[0]
        print len(o), o
        return render_template("index.html", problem=thewkt)
    return render_template("index.html")


