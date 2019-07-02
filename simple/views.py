from simple import app

import runvalidation

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, _app_ctx_stack
from werkzeug.utils import secure_filename
import os
import subprocess
import uuid
import time
import json
import copy
from geoip import geolite2

TRUSTED_PROXIES = {'127.0.0.1'}  

ALLOWED_EXTENSIONS = set(['gml', 'xml', 'obj', 'poly', 'json', 'off'])


ALLOWED_EXTENSIONS = set(['gml', 'xml'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def verify_tolerance(t, defaultval):
    t = t.replace(',', '.')
    d = float(defaultval)
    try:
      re = float(t)
      if (re >= 0.0):
        return re
      return d
    except:
      return d



@app.route('/about')
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    os.chdir(app.config['VAL3DITYEXE_FOLDER'])
    cmd = []
    cmd.append("./val3dity")
    cmd.append("--version")
    op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    R = op.poll()
    if R:
        res = op.communicate()
        raise ValueError(res[1])
    val3dityversion = op.communicate()[0].split()[2]
    if request.method == 'POST':
        f = request.files['file']
        if f:
            if allowed_file(f.filename):
                route = request.access_route + [request.remote_addr]
                clientip = next((addr for addr in reversed(route) if addr not in TRUSTED_PROXIES), request.remote_addr)
                fname = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                # print os.path.join(app.config['UPLOAD_FOLDER'], fname)
                snap_tol = verify_tolerance(request.form['snap_tol'], '1e-3')
                planarity_d2p_tol = verify_tolerance(request.form['planarity_d2p_tol'], '1e-2')
                overlap_tol = verify_tolerance(request.form['overlap_tol'], '-1')
                prim3d = request.form['prim3d']
                ignore204 = 'ignore204' in request.form
                geom_is_sem_surfaces = 'geom_is_sem_surfaces' in request.form
                uploadtime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())

                jid = str(uuid.uuid4())
                summary = runvalidation.validate(
                    jid, 
                    app.config['UPLOAD_FOLDER']+fname, 
                    snap_tol, 
                    planarity_d2p_tol, 
                    overlap_tol, 
                    prim3d,
                    ignore204,
                    geom_is_sem_surfaces, 
                    app.config['VAL3DITYEXE_FOLDER'],    
                    app.config['REPORTS_FOLDER'])    
                print summary
                os.remove(app.config['UPLOAD_FOLDER']+fname)
           
                return redirect('/simple/reports/%s' % jid)
            else:
                return render_template("index.html", problem='Uploaded file is not a valid file.', version=val3dityversion)
        else:
            return render_template("index.html", problem='No file selected.', version=val3dityversion)
    return render_template("index.html", version=val3dityversion)

@app.route('/stats')
def stats():
    totaljobs   = query_db('select count(*) from tasks', [], one=True)
    totalsolids = query_db('select sum(total_primitives) from tasks', [], one=True)
    totalinvalidsolids = query_db('select sum(invalid_primitives) from tasks', [], one=True)
    percentage = int((float(totalinvalidsolids[0]) / float(totalsolids[0])) * 100)
    last5 = query_db('select * from tasks order by timestamp desc limit 5', [], one=False)
    a = []
    for each in last5:
      ipcountry = 'unknown'
      if (each['ip'] is not None): 
        ipobj = geolite2.lookup(each['ip'])
        if ipobj is not None:
          ipcountry = ipobj.country
      a.append((each['timestamp'].replace("T", " "), each['total_primitives'], each['invalid_primitives'], each['errors'], ipcountry))
    allerrors = query_db('select errors from tasks where errors is not null and errors!=-1', [])
    myerr = {}
    for es in allerrors:
      tmp = es[0].split("-")
      ei = map(int, tmp)
      for e in ei:
        if e not in myerr:
          myerr[e] = 1
        else:
          myerr[e] += 1
    higherr = 100;
    highest = 0;
    for e in myerr:
      if myerr[e] > highest:
        highest = myerr[e]
        higherr = e
    return render_template("stats.html", 
                           totaljobs="{:,}".format(totaljobs[0]),
                           totalsolids="{:,}".format(totalsolids[0]),
                           totalinvalidsolids="{:,}".format(totalinvalidsolids[0]),
                           percentageinvalids=percentage,
                           mosterror=higherr,
                           last5=a
                          )





