from prepair import app
from settings import *

from flask import render_template, request, redirect, url_for
import os
import subprocess

MAXSIZE = 1e4


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/', methods=['GET', 'POST'])
def index():
    print "hugo"
    if request.method == 'POST':
        thewkt = request.form['thewkt']
        if thewkt == "":
            return render_template("index.html", problem="Error: no WKT given.")
        if len(thewkt) > MAXSIZE:
            return render_template("index.html", problem="Error: WKT too big (max allowed is %d char)." % MAXSIZE)
        cmd = []
        cmd.append(PREPAIREXE)
        cmd.append("--wkt")
        cmd.append(r"%s" % thewkt)
        op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        R = op.poll()
        if R:
          res = op.communicate()
          raise ValueError(res[1])
        # o = op.communicate()[0]
        o = op.communicate()
        if (o[0] != ""):
            return render_template("index.html", success = o[0])
        else:
            if o[1] == "":
                return render_template("index.html", problem="Error: something went wrong. Check the input WKT.")
            return render_template("index.html", problem=o[1])
    return render_template("index.html")


