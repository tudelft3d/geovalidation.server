from val3dity2 import app
from val3dity2 import celery

import runvalidation

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, _app_ctx_stack
from werkzeug.utils import secure_filename
import os
import subprocess
import uuid
import time
import copy
from geoip import geolite2

TRUSTED_PROXIES = {'127.0.0.1'}  

ALLOWED_EXTENSIONS = set(['gml', 'xml', 'obj', 'poly', 'json', 'off'])


@celery.task
def validate(fname, 
             snap_tol, 
             planarity_d2p_tol, 
             overlap_tol, 
             prim3d, 
             ignore204, 
             geom_is_sem_surfaces, 
             uploadtime):
    summary = runvalidation.validate(validate.request.id, 
                                     fname, 
                                     snap_tol, 
                                     planarity_d2p_tol, 
                                     overlap_tol, 
                                     prim3d,
                                     ignore204,
                                     geom_is_sem_surfaces, 
                                     app.config['VAL3DITYEXE_FOLDER'],    
                                     app.config['REPORTS_FOLDER'])    
    #-- write summary to database
    print summary
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    db.execute('update tasks set validated=?, total_primitives=?, invalid_primitives=?, total_cityobjects=?, invalid_cityobjects=?, errors=? where jid=?',
               [
               1,
               summary['total_primitives'], 
               summary['invalid_primitives'], 
               summary['total_cityobjects'], 
               summary['invalid_cityobjects'], 
               summary['errors'], 
               validate.request.id])
    db.commit()
    db.close()
    #-- rm the uploaded file
    os.remove(fname) 
    return True

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
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/stats')
def stats():
    totaljobs   = query_db('select count(*) from tasks', [], one=True)
    totalsolids = query_db('select sum(noprimitives) from tasks', [], one=True)
    totalinvalidsolids = query_db('select sum(noinvalid) from tasks', [], one=True)
    percentage = int((float(totalinvalidsolids[0]) / float(totalsolids[0])) * 100)
    last5 = query_db('select * from tasks order by timestamp desc limit 5', [], one=False)
    a = []
    for each in last5:
      ipcountry = 'unknown'
      if (each['ip'] is not None): 
        ipobj = geolite2.lookup(each['ip'])
        if ipobj is not None:
          ipcountry = ipobj.country
      a.append((each['timestamp'].replace("T", " "), each['noprimitives'], each['noinvalid'], each['errors'], ipcountry))
    allerrors = query_db('select errors from tasks where errors is not null and errors!=-1', [])
    myerr = copy.deepcopy(dErrors)
    for each in myerr:
      myerr[each] = 0;
    for es in allerrors:
      tmp = es[0].split("-")
      ei = map(int, tmp)
      for e in ei:
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
                           mosterrordef=dErrors[higherr],
                           last5=a
                          )
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET', 'POST'])
def index():
    os.chdir("/Users/hugo/projects/val3dity")
    cmd = []
    cmd.append("git")
    cmd.append("rev-parse")
    cmd.append("HEAD")
    op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    R = op.poll()
    if R:
      res = op.communicate()
      raise ValueError(res[1])
    gitcommit = "https://github.com/tudelft3d/val3dity/commit/" + op.communicate()[0]
    if request.method == 'POST':
        f = request.files['file']
        if f:
            if allowed_file(f.filename):
              route = request.access_route + [request.remote_addr]
              clientip = next((addr for addr in reversed(route) if addr not in TRUSTED_PROXIES), request.remote_addr)
              fname = secure_filename(f.filename)
              f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
              snap_tol = verify_tolerance(request.form['snap_tol'], '1e-3')
              planarity_d2p_tol = verify_tolerance(request.form['planarity_d2p_tol'], '1e-2')
              overlap_tol = verify_tolerance(request.form['overlap_tol'], '-1')
              prim3d = request.form['prim3d']
              ignore204 = 'ignore204' in request.form
              geom_is_sem_surfaces = 'geom_is_sem_surfaces' in request.form
              uploadtime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
              celtask = validate.delay(app.config['UPLOAD_FOLDER']+fname, 
                                       snap_tol, 
                                       planarity_d2p_tol, 
                                       overlap_tol, 
                                       prim3d, 
                                       ignore204, 
                                       geom_is_sem_surfaces, 
                                       uploadtime)

              jid = celtask.id
              db = get_db()
              db.execute('insert into tasks (jid, file, timestamp, ip, validated) values (?, ?, ?, ?, ?)',
                        [jid, 
                        fname, 
                        uploadtime,
                        clientip,
                        0])
              db.commit()
              return redirect('/val3dity2/reports/%s' % jid)
            else:
              return render_template("index.html", problem='Uploaded file is not a valid file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html", version=gitcommit)


@app.route('/reports/<jobid>')
def reports(jobid):
    #-- check if job is in the database
    db = query_db('select * from tasks where jid = ?', [jobid], one=True)
    if db is None:
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    #-- it exists
    fname = db['file']
    print fname
    if (db['validated'] == 0):
        celtask = celery.AsyncResult(jobid)
        if (celtask.ready() == False):
            print "task not finished."
            return render_template("status.html", notask=False, info='Validation in progress: %s' % fname, refresh=True)
    if (db['total_primitives'] > 0) and (db['invalid_primitives'] == 0) and (db['total_cityobjects'] > 0) and (db['invalid_cityobjects'] == 0) :
        return render_template("report.html", 
                               filename=fname, 
                               jid=jobid, 
                               total_primitives=db["total_primitives"], 
                               invalid_primitives=db["invalid_primitives"], 
                               total_cityobjects=db["total_cityobjects"], 
                               invalid_cityobjects=db["invalid_cityobjects"], 
                               welldone=True) 
    else:
        return render_template("report.html", 
                             filename=fname, 
                             jid=jobid, 
                             total_primitives=db["total_primitives"], 
                             invalid_primitives=db["invalid_primitives"], 
                             total_cityobjects=db["total_cityobjects"], 
                             invalid_cityobjects=db["invalid_cityobjects"], 
                             welldone=False)
        

@app.route('/reports/download/<jobid>')
def reports_download(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.json' % jobid)


