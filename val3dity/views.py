from val3dity import app


from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, _app_ctx_stack
from werkzeug.utils import secure_filename
import os
import subprocess
import uuid
import time
import json


from .runvalidation import validate

TRUSTED_PROXIES = {'127.0.0.1'}  

ALLOWED_EXTENSIONS = set(['gml', 'xml', 'obj', 'poly', 'json', 'off'])


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
    val3dityversion = (op.communicate()[0].split()[2]).decode('UTF-8')
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
                uploadtime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
                jid = str(uuid.uuid4())
                validate(
                    jid, 
                    app.config['UPLOAD_FOLDER']+fname, 
                    snap_tol, 
                    planarity_d2p_tol, 
                    overlap_tol, 
                    app.config['VAL3DITYEXE_FOLDER'],    
                    app.config['REPORTS_FOLDER'])    
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
    ftype = j["input_file_type"]
    success = j["validity"]
    ft = 0
    fi = 0
    for f in j["features_overview"]:
        ft += f["total"]
        fi += f["total"] - f["valid"]
    pt = 0
    pi = 0
    for p in j["primitives_overview"]:
        pt += p["total"]
        pi += p["total"] - p["valid"]        
    return render_template("report.html", 
                           filename=fname, 
                           filetype=ftype,
                           jid=jobid, 
                           total_primitives=pt, 
                           invalid_primitives=pi, 
                           total_features=ft, 
                           invalid_features=fi, 
                           welldone=success) 
    

@app.route('/reports/download/<jobid>')
def reports_download(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.json' % jobid)

