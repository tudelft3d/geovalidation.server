from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import time

ROOT_FOLDER        = '/Users/hugo/www/geovalidation/'
UPLOAD_FOLDER      = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER     = ROOT_FOLDER + 'reports/'
STATIC_FOLDER      = ROOT_FOLDER + 'static/'
ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER


# @app.route("/")
# def index():
#     return render_template("index.html")

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


# return app.send_static_file('index.html')
# return send_from_directory('/Users/hugo/Dropbox/temp/flask', 'index.html')
# return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)
# return redirect(url_for('uploaded_file', filename=fname))

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



# @app.route('/static/<path:filename>')
# def send_foo(filename):
#     return send_from_directory(STATIC_FOLDER, filename)


@app.route('/', methods=['GET', 'POST'])
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
            return render_template("uploaded.html", id=jid)
        else:
            return render_template("info.html", title='ERROR', info1='File not of GML/XML type.')
    return render_template("index.html")


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@app.route('/reports/download/<jobid>')
def download_report(jobid):
    return send_from_directory(app.config['REPORTS_FOLDER'], '%s.xml' % jobid)


@app.route('/reports/<jobid>')
def show_post(jobid):
    fs = "%s%s.txt" % (REPORTS_FOLDER, jobid)
    fr = "%s%s.xml" % (REPORTS_FOLDER, jobid)
    if not os.path.exists(fs):
        return render_template("info.html", title='ERROR', info1='Error: no such report or the process is not finished.', info2='Be patient.')
    else:
        summary = open(fs, "r").read().split('\n')
        report = open(fr, "r")
        print summary
        report.readline()
        tmp = report.readline()
        fname = (tmp.split(">")[1]).split("<")[0]
        s = '<h2>Report for file %s</h2>' % fname
        if len(summary) == 1:
          s += '<p><FONT COLOR="#fa1b33">%s</FONT></p>' % summary[0]
        else:
          s += '<p>%s</p>' % summary[0]
          s += '<p>%s</p>' % summary[1]
          if (summary[2] == 'Hourrraaa!'):
              if (summary[0] != 'Number of solids in file: 0'):
                  s += '<img src="/static/welldone.png" width="120" alt="">'
          else:
              s += "<p>%s (<a href='/errors'>overview of the possible errors</a>)</p><ul>" % summary[2]
          for er in summary[3:]:
            if (er != ''):
              s += '<li>%s</li>' % er
          s += "</ul>"
        s += "<p><a href='/reports/download/%s'>%s.xml</a></p>" % (jobid, jobid)
        return wwwheader + s + wwwfooter

if __name__ == '__main__':
    app.run(debug=True) # TODO: no debug in release mode!



