from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import time

ROOT_FOLDER        = '/Users/hugo/www/geovalidation/'
UPLOAD_FOLDER      = ROOT_FOLDER + 'uploads/'
TMP_FOLDER         = ROOT_FOLDER + 'tmp/'
REPORTS_FOLDER     = ROOT_FOLDER + 'reports/'
STATIC_FOLDER      = ROOT_FOLDER + 'static/'

ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER']  = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER
app.config['TMP_FOLDER']     = TMP_FOLDER


# return app.send_static_file('index.html')
# return send_from_directory('/Users/hugo/Dropbox/temp/flask', 'index.html')
# return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)
# return redirect(url_for('uploaded_file', filename=fname))

# @app.route('/val3dity/static/<path:filename>')
# def send_foo(filename):
#     return send_from_directory(STATIC_FOLDER, filename)


@app.route('/val3dity/errors')
def errors():
    return render_template("val3dity/errors.html")

@app.route('/val3dity/about')
def about():
    return render_template("val3dity/about.html")

@app.route('/val3dity/contact')
def contact():
    return render_template("val3dity/contact.html")
    
@app.route('/val3dity/faq')
def faq():
    return render_template("val3dity/faq.html")

@app.route('/')
def root():
    # return render_template("val3dity/info.html")
    return redirect('/val3dity')

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


@app.route('/val3dity/addgmlids', methods=['GET', 'POST'])
def addgmlids():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            print fname
            n = os.path.join(app.config['TMP_FOLDER'], fname)
            f.save(n)
            n2 = n[:-4] + ".id.xml"
            os.system("python /Users/hugo/projects/val3dity/ressources/python/addgmlids.py %s %s" % (n, n2))
            # print '%s.id.xml' % fname[:-4]
            return send_from_directory(app.config['TMP_FOLDER'], '%s.id.xml' % fname[:-4])
        else:
            return render_template("val3dity/info.html", title='ERROR', info1='File not of GML/XML type.')
    return render_template("val3dity/addgmlids.html")


@app.route('/val3dity', methods=['GET', 'POST'])
def upload_file():
    # global jobid
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            snap_tolerance = verify_snap_tolerance(request.form['snap_tolerance'])
            jid = get_job_id()
            fjob = open("%s%s.txt" % (UPLOAD_FOLDER, jid), 'w')
            fjob.write("%s\n" % fname)
            fjob.write("%s\n" % snap_tolerance)
            fjob.write("%s\n" % time.asctime())
            fjob.close()
            return render_template("val3dity/uploaded.html", id=jid)
        else:
            return render_template("val3dity/info.html", title='ERROR', info1='File not of GML/XML type.')
    return render_template("val3dity/index.html")


@app.route('/val3dity/reports/download/<jobid>')
def download_report(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.xml' % jobid)


@app.route('/val3dity/reports/<jobid>')
def show_post(jobid):
    fs = "%s%s.txt" % (REPORTS_FOLDER, jobid)
    fr = "%s%s.xml" % (REPORTS_FOLDER, jobid)
    if not os.path.exists(fs):
        return render_template("val3dity/info.html", title='ERROR', info1='Error: no such report or the process is not finished.', info2='Be patient.', refresh=True)
    else:
        summary = open(fs, "r").read().split('\n')
        report = open(fr, "r")
        print summary
        report.readline()
        tmp = report.readline()
        fname = (tmp.split(">")[1]).split("<")[0]
        if len(summary) == 1:
            return render_template("val3dity/report.html", 
                                  problems='%s'%summary[0],
                                  filename=fname,
                                  jid=jobid
                                  )
        else:
            if (summary[2] == 'Hourrraaa!'):
                return render_template("val3dity/report.html", 
                                      filename=fname,
                                      jid=jobid,
                                      summary0=summary[0], 
                                      summary1=summary[1],
                                      welldone=True 
                                      )
            else:
                print summary[3:-1]
                return render_template("val3dity/report.html", 
                                      filename=fname,
                                      jid=jobid,
                                      summary0=summary[0], 
                                      summary1=summary[1],
                                      errors=summary[3:-1]
                                      )
 

if __name__ == '__main__':
    app.run(debug=True) # TODO: no debug in release mode!


