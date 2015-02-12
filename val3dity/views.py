from val3dity import app
from val3dity import celery
from settings import *

import runvalidation


from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, _app_ctx_stack
from werkzeug.utils import secure_filename
import os
import uuid
import time

ALLOWED_EXTENSIONS = set(['gml', 'xml'])


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

@celery.task
def validate(fname, primitives, snaptol, plantol):
    totalxml, summary = runvalidation.validate(UPLOAD_FOLDER+fname, primitives, snaptol, plantol)    
    print summary
    return True
    # print "yo celery", file
    # time.sleep(10)

    return file

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


def get_job_id():
    return str(uuid.uuid4())
    # return str(uuid.uuid4()).split('-')[0]


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
            os.system("%s %s %s" % (ADDGMLIDS_EXE, n, n2))
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


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            if allowed_file(f.filename):
              fname = secure_filename(f.filename)
              f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
              primitives = request.form['primitives']
              snaptol = verify_tolerance(request.form['snaptol'], '1e-3')
              plantol = verify_tolerance(request.form['plantol'], '1e-2')
              uploadtime = time.localtime()
              celtask = validate.delay(fname, primitives, snaptol, plantol)    
              # celtask = runvalidation.validate.delay(fname, primitives, snaptol, plantol)    
              jid = celtask.id

              db = get_db()
              db.execute('insert into tasks (jid, file, primitives, snaptol, plantol, timestamp) values (?, ?, ?, ?, ?, ?)',
                        [jid, 
                        fname, 
                        request.form['primitives'], 
                        snaptol, 
                        plantol, 
                        time.strftime('%Y-%m-%dT%H:%M:%S', uploadtime)])
              db.commit()
              return render_template("index.html", jobid=jid)
            else:
              return render_template("index.html", problem='Uploaded file is not a GML file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html")


@app.route('/reports/<jobid>')
def reports(jobid):
    #-- check if job is in the database
    j = query_db('select * from tasks where jid = ?', [jobid], one=True)
    if j is None:
        return render_template("status.html", success=False, info1="Error: this report number doesn't exist.", refresh=False)
    #-- it exists
    # print '---', j['timestamp']
    celtask = celery.AsyncResult(jobid)
    if (celtask.ready() == False):
        return render_template("status.html", success=False, info1='Tasks not finished.', info2='Be patient.', refresh=True)
    # print celtask.result
    return render_template("status.html", success=False, info1='done, finished.', info2='great', refresh=False)


@app.route('/reports/download/<jobid>')
def reports_download(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.xml' % jobid)


@app.route('/reports_2/<jobid>')
def reports_2(jobid):
    fs = "%s%s.txt" % (REPORTS_FOLDER, jobid)
    fr = "%s%s.xml" % (REPORTS_FOLDER, jobid)
    if not os.path.exists(fs):
        return render_template("status.html", success=False, info1='No such report or the process is not finished.', info2='Be patient.', refresh=True)
    else:
        summary = open(fs, "r").read().split('\n')
        report = open(fr, "r")
        print summary
        report.readline()
        tmp = report.readline()
        fname = (tmp.split(">")[1]).split("<")[0]
        if len(summary) == 1:
            return render_template("report.html", 
                                  problems='%s'%summary[0],
                                  filename=fname,
                                  welldone=False,
                                  jid=jobid
                                  )
        else:
            if ( (summary[0][-2:] != ' 0') and (summary[2] == 'Hourrraaa!') ):
                return render_template("report.html", 
                                      filename=fname,
                                      jid=jobid,
                                      summary0=summary[0], 
                                      summary1=summary[1],
                                      welldone=True 
                                      )
            elif ( (summary[0][-2:] == ' 0') and (summary[2] == 'Hourrraaa!') ):
                return render_template("report.html", 
                                      filename=fname,
                                      jid=jobid,
                                      summary0=summary[0], 
                                      summary1=summary[1],
                                      zeroprimitives=True,
                                      welldone=False 
                                      )
            else:
                print summary[3:-1]
                return render_template("/report.html", 
                                      filename=fname,
                                      jid=jobid,
                                      summary0=summary[0], 
                                      summary1=summary[1],
                                      errors=summary[3:-1]
                                      )
 