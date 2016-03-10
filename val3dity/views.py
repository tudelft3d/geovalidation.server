from val3dity import app
from val3dity import celery

import runvalidation

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, _app_ctx_stack
from werkzeug.utils import secure_filename
import os
import uuid
import time

ALLOWED_EXTENSIONS = set(['gml', 'xml'])


dErrors = {
  101: "TOO_FEW_POINTS",
  102: "CONSECUTIVE_POINTS_SAME",
  103: "RING_NOT_CLOSED",
  104: "RING_SELF_INTERSECTION",
  105: "RING_COLLAPSED",
  201: "INTERSECTION_RINGS",
  202: "DUPLICATED_RINGS",
  203: "NON_PLANAR_POLYGON_DISTANCE_PLANE",
  204: "NON_PLANAR_POLYGON_NORMALS_DEVIATION",
  205: "POLYGON_INTERIOR_DISCONNECTED",
  206: "HOLE_OUTSIDE",
  207: "INNER_RINGS_NESTED",
  208: "ORIENTATION_RINGS_SAME",
  300: "NOT_VALID_2_MANIFOLD",
  301: "TOO_FEW_POLYGONS",
  302: "SHELL_NOT_CLOSED",
  303: "NON_MANIFOLD_VERTEX",
  304: "NON_MANIFOLD_EDGE",
  305: "MULTIPLE_CONNECTED_COMPONENTS",
  306: "SHELL_SELF_INTERSECTION",
  307: "POLYGON_WRONG_ORIENTATION",
  308: "ALL_POLYGONS_WRONG_ORIENTATION",
  309: "VERTICES_NOT_USED",
  401: "SHELLS_FACE_ADJACENT",
  402: "INTERSECTION_SHELLS",
  403: "INNER_SHELL_OUTSIDE_OUTER",
  404: "SOLID_INTERIOR_DISCONNECTED",
  901: "INVALID_INPUT_FILE",
  902: "EMPTY_PRIMITIVE",
  999: "UNKNOWN_ERROR",
}


@celery.task
def validate(fname, primitives, snaptol, plantol, uploadtime):
    summary = runvalidation.validate(validate.request.id, 
                                     fname,
                                     primitives,
                                     snaptol,
                                     plantol,
                                     app.config['VAL3DITYEXE_FOLDER'],    
                                     app.config['UPLOAD_FOLDER'])    
    #-- write summary to database
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    db.execute('update tasks set noprimitives=?, noinvalid=?, errors=? where jid=?',
              [summary['noprimitives'], 
              summary['noinvalid'], 
              summary['errors'], 
              validate.request.id])
    db.commit()
    db.close()
    #-- write summary to database
    s = "%s%s.xml" % (app.config['REPORTS_FOLDER'], validate.request.id)        
    fout = open(s, 'w')
    fout.write('\n'.join(reportxml))
    fout.close()
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

@app.route('/errors')
def errors():
    return render_template("errors.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

    
@app.route('/faq')
def faq():
    return render_template("faq.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/addgmlids', methods=['GET', 'POST'])
def addgmlids():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            print fname
            n = os.path.join(app.config['TMP_FOLDER'], fname)
            f.save(n)
            n2 = n[:-4] + ".id.xml"
            os.system("%s %s %s" % (app.config['ADDGMLIDSEXE'], n, n2))
            return send_from_directory(app.config['TMP_FOLDER'], '%s.id.xml' % fname[:-4])
        else:
            return render_template("status.html", success=False, info1='Uploaded file is not a GML file.')
    return render_template("addgmlids.html")


@app.route('/_problemfiles', methods=['GET', 'POST'])
def problemfiles():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            print fname
            n = os.path.join(app.config['PROBLEMFILES_FOLDER'], fname)
            print n
            f.save(n)
            return render_template("problemfiles.html", done=True)
    return render_template("problemfiles.html")


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
    if request.method == 'POST':
        f = request.files['file']
        if f:
            if allowed_file(f.filename):
              fname = secure_filename(f.filename)
              print "1"
              f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
              primitives = request.form['primitives']
              snaptol = verify_tolerance(request.form['snaptol'], '1e-3')
              plantol = verify_tolerance(request.form['plantol'], '1e-2')
              uploadtime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
              celtask = validate.delay(app.config['UPLOAD_FOLDER']+fname, primitives, snaptol, plantol, uploadtime)    
              jid = celtask.id
              db = get_db()
              db.execute('insert into tasks (jid, file, primitives, snaptol, plantol, timestamp) values (?, ?, ?, ?, ?, ?)',
                        [jid, 
                        fname, 
                        request.form['primitives'], 
                        snaptol, 
                        plantol, 
                        uploadtime])
              db.commit()
              # return render_template("index.html", jobid=jid)
              return redirect('/val3dity/reports/%s' % jid)
            else:
              return render_template("index.html", problem='Uploaded file is not a valid file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html")


@app.route('/reports/<jobid>')
def reports(jobid):
    #-- check if job is in the database
    j = query_db('select * from tasks where jid = ?', [jobid], one=True)
    if j is None:
        return render_template("status.html", notask=True, info="Error: this report number doesn't exist.", refresh=False)
    #-- it exists
    fname = j['file']
    print fname
    if j['noprimitives'] is None:
        celtask = celery.AsyncResult(jobid)
        if (celtask.ready() == False):
            print "task not finished."
            return render_template("status.html", notask=False, info='Validation in progress: %s' % fname, refresh=True)
    if (j['errors'] == '901'):
        return render_template("report.html", 
                              filename=fname,
                              jid=jobid,
                              noprimitives=0, 
                              noinvalid=0,
                              zeroprimitives=False,
                              badinput=True,
                              welldone=False 
                              )    
    if (j['noprimitives'] == 0):
        return render_template("report.html", 
                              filename=fname,
                              jid=jobid,
                              noprimitives=0, 
                              noinvalid=0,
                              zeroprimitives=True,
                              welldone=False 
                              )
    if (j['noprimitives'] > 0) and (j['noinvalid'] == 0):
        return render_template("report.html", 
                               filename=fname, 
                               jid=jobid, 
                               noprimitives=j['noprimitives'], 
                               noinvalid=0, 
                               zeroprimitives=False, 
                               welldone=True) 
    else:
        s = j['errors'].split('-')
        errors = map(int, s)
        errors.sort()
        lserrors = [] 
        for e in errors:
            description = dErrors[e]
            errors = str(e) + " -- " + description
            lserrors.append(errors)
        print lserrors

        return render_template("report.html", 
                              filename=fname,
                              jid=jobid,
                              noprimitives=j['noprimitives'], 
                              noinvalid=j['noinvalid'],
                              zeroprimitives=False,
                              errors=lserrors,
                              welldone=False 
                              )


@app.route('/reports/download/<jobid>')
def reports_download(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.xml' % jobid)


