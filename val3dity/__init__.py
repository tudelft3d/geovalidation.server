
from flask import Flask

LOCAL = True

if LOCAL == True:
  ROOT_FOLDER        = '/Users/hugo/www/geovalidation/val3dity/'
else:
  ROOT_FOLDER        = '/var/www/geovalidation/'

UPLOAD_FOLDER       = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER      = ROOT_FOLDER + 'reports/'
PROBLEMFILES_FOLDER = ROOT_FOLDER + 'problemfiles/'
TMP_FOLDER          = ROOT_FOLDER + 'tmp/'
STATIC_FOLDER       = ROOT_FOLDER + 'static/'

ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER']       = UPLOAD_FOLDER
app.config['REPORTS_FOLDER']      = REPORTS_FOLDER
app.config['PROBLEMFILES_FOLDER'] = PROBLEMFILES_FOLDER
app.config['TMP_FOLDER']          = TMP_FOLDER

from val3dity import app
from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import time

# return app.send_static_file('index.html')
# return send_from_directory('/Users/hugo/Dropbox/temp/flask', 'index.html')
# return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)
# return redirect(url_for('uploaded_file', filename=fname))

# @app.route('/static/<path:filename>')
# def send_foo(filename):
#     return send_from_directory(STATIC_FOLDER, filename)


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


def verify_snap_tolerance(t):
    t = t.replace(',', '.')
    d = float(1e-3)
    try:
      re = float(t)
      if (re >= 0.0):
        return re
      return d
    except:
      return d


def get_job_id():
    return str(uuid.uuid4()).split('-')[0]


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
            if LOCAL == True:
              os.system("python /Users/hugo/projects/val3dity/ressources/python/addgmlids.py %s %s" % (n, n2))
            else:
              os.system("python /home/hledoux/projects/val3dity/ressources/python/addgmlids.py %s %s" % (n, n2))
            # print '%s.id.xml' % fname[:-4]
            return send_from_directory(app.config['TMP_FOLDER'], '%s.id.xml' % fname[:-4])
        else:
            return render_template("status.html", success=False, info1='File not of GML/XML type.')
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

@app.route('/', methods=['GET', 'POST'])
def index():
    # global jobid
    if request.method == 'POST':
        f = request.files['file']
        if f:
            if  allowed_file(f.filename):
              fname = secure_filename(f.filename)
              f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
              snap_tolerance = verify_snap_tolerance(request.form['snap_tolerance'])
              jid = get_job_id()
              fjob = open("%s%s.txt" % (UPLOAD_FOLDER, jid), 'w')
              fjob.write("%s\n" % fname)
              fjob.write("%s\n" % snap_tolerance)
              fjob.write("%s\n" % time.asctime())
              fjob.close()
              return render_template("index.html", jobid=jid)
            else:
              return render_template("index.html", problem='Uploaded file is not of a GML file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html")


@app.route('/reports/download/<jobid>')
def reports_download(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.xml' % jobid)


@app.route('/reports/<jobid>')
def reports(jobid):
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
            if (summary[2] == 'Hourrraaa!'):
                return render_template("report.html", 
                                      filename=fname,
                                      jid=jobid,
                                      summary0=summary[0], 
                                      summary1=summary[1],
                                      welldone=True 
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
 

# if __name__ == '__main__':
#   if LOCAL == True:
#     app.run(debug=True) # TODO: no debug in release mode!
#   else:
#     app.run() 




