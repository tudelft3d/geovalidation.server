from val3dity import app

import runvalidation

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, _app_ctx_stack
from werkzeug.utils import secure_filename
import os
import subprocess
import uuid
import time
import json
import copy


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
                return redirect('/val3dity/reports/%s' % jid)
            else:
                return render_template("index.html", problem='Uploaded file is not a valid file.', version=val3dityversion)
        else:
            return render_template("index.html", problem='No file selected.', version=val3dityversion)
    return render_template("index.html", version=val3dityversion)



@app.route('/reports/<jobid>')
def reports(jobid):
    #-- check if file exists
    if (os.path.isfile(app.config['REPORTS_FOLDER'] + jobid + ".json") == False):
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    j = json.loads(open(app.config['REPORTS_FOLDER'] + jobid + ".json").read())
    fname = j["input_file"]
    fname = fname[fname.rfind('/')+1:]
    if j["invalid_primitives"] == 0 and j["invalid_features"] == 0:
        success = True
    else:
        success = False
    return render_template("report.html", 
                           filename=fname, 
                           jid=jobid, 
                           total_primitives=j["total_primitives"], 
                           invalid_primitives=j["invalid_primitives"], 
                           total_features=j["total_features"], 
                           invalid_features=j["invalid_features"], 
                           welldone=success) 
    

@app.route('/reports/download/<jobid>')
def reports_download(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.json' % jobid)


@app.route('/reports/overview/<jobid>')
def reports_overview(jobid):
    #-- check if file exists
    if (os.path.isfile(app.config['REPORTS_FOLDER'] + jobid + ".json") == False):
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    #-- it exists
    j = json.loads(open(app.config['REPORTS_FOLDER'] + jobid + ".json").read())
    return render_template("report_overview.html", thereport=j, myjobid=jobid) 

@app.route('/reports/features/<jobid>')
def reports_features(jobid):
    if (os.path.isfile(app.config['REPORTS_FOLDER'] + jobid + ".json") == False):
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    j = json.loads(open(app.config['REPORTS_FOLDER'] + jobid + ".json").read())
    return render_template("tree.html", thereport=j) 


@app.route('/reports/cityobjects/<jobid>')
def reports_cityobjects(jobid):
    if (os.path.isfile(app.config['REPORTS_FOLDER'] + jobid + ".json") == False):
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    j = json.loads(open(app.config['REPORTS_FOLDER'] + jobid + ".json").read())
    return render_template("report_CityObjects.html", thereport=j) 


@app.route('/reports/primitives/<jobid>')
def reports_primitives(jobid):
    if (os.path.isfile(app.config['REPORTS_FOLDER'] + jobid + ".json") == False):
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    j = json.loads(open(app.config['REPORTS_FOLDER'] + jobid + ".json").read())
    return render_template("report_Primitives.html", thereport=j)   

