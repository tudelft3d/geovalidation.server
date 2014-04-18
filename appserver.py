from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pickle
import time
import sqlite3

ROOT_FOLDER        = '/Users/hugo/www/geovalidation/'
UPLOAD_FOLDER      = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER     = ROOT_FOLDER + 'reports/'
STATIC_FOLDER      = ROOT_FOLDER + 'static/'
ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER


conn = sqlite3.connect('alljobs.db', check_same_thread = False)
c = conn.cursor()


wwwheader = """
<html>
  <head>
    <link href='http://fonts.googleapis.com/css?family=Inconsolata' rel='stylesheet' type='text/css'>
    <style>
      body {
        font-family: 'Inconsolata', null;
        background-color: #fafafa;
        font-color: #2df5dd;
        padding-top: 50px;
        text-align: left;
      }
      h1 {
        font-size: 32px;
        padding-top: 50px;
        text-align: left;
      }
      h2 {
        font-size: 28px;
      }      
      h3 {
        font-size: 24px;
      }
      p,ul {
        font-family: 'Inconsolata', null;
        font-size: 18px;
        background-color: #fafafa;
        font-color: #2df5dd;
        text-align: left; 
      }
      #wrapper{
        width: 700px;
        margin: 0 auto;
      }
      #footer{
        margin: 0 auto;
        width: 700px;
        padding-top: 20px;
        text-align: right;
        font-size: 14px;
      }
    </style>
  </head>
  <body>
  <div id="wrapper">
"""

wwwfooter = """
  </div>
  <div id="footer">
    <hr/>
    <a href="/">home</a> 
    <a href="/about">about</a> 
    <a href="/faq">faq</a> 
    <a href="/contact">contact</a> 
  </div>
  </body>
</html>
"""

wwwerrors = """
  <h2 id="errorreported">Error reported</h2>
  <h3 id="ringlevel">Ring level</h3>
    <ul>
    <li>100: REPEATED_POINTS</li>
    <li>110: RING_NOT_CLOSED</li>
    <li>120: RING_SELF_INTERSECT</li>
    </ul>
  <h3 id="surfacelevel">Surface level (one polygon embedded in 3D)</h3>
    <ul>
    <li>200: SELF_INTERSECTION</li>
    <li>210: NON_PLANAR_SURFACE</li>
    <li>220: INTERIOR_DISCONNECTED</li>
    <li>230: HOLE_OUTSIDE</li>
    <li>240: HOLES_ARE_NESTED</li>
    <li>250: ORIENTATION_RINGS_SAME</li>
    </ul>
  <h3 id="shelllevel">Shell level (one envelop formed by several surfaces)</h3>
    <ul>
    <li>300: NOT_VALID_2_MANIFOLD
    <ul>
    <li>301: SURFACE_NOT_CLOSED</li>
    <li>302: DANGLING_FACES</li>
    <li>303: FACE_ORIENTATION_INCORRECT_EDGE_USAGE</li>
    <li>304: FREE_FACES</li>
    <li>305: SURFACE_SELF_INTERSECTS</li>
    <li>306: VERTICES_NOT_USED</li>
    </ul></li>
    <li>310: SURFACE_NORMALS_WRONG_ORIENTATION</li>
    </ul>
  <h3 id="solidlevel">Solid level (1 exterior shell + 0..n exterior shells)</h3>
    <ul>
    <li>400: SHELLS_FACE_ADJACENT</li>
    <li>410: SHELL_INTERIOR_INTERSECT</li>
    <li>420: INNER_SHELL_OUTSIDE_OUTER</li>
    <li>430: INTERIOR_OF_SHELL_NOT_CONNECTED</li>
  </ul>
"""

wwwindex = """
  <title>val3dity: geometric validation of solids according to ISO19107</title>
    <h1><img src="/static/val3dity.png" width=250 alt=""/><br>geometric validation of GML solids</h1>
    <form action="" method=post enctype=multipart/form-data>
      <ol>
        <li><input type=file name=file></li>
        <li>snapping tolerance for vertices: <input type="text" name="snap_tolerance" value="1e-3" maxlength="10" align="right"></li>
        <li><input type=submit value="upload + validate"></li>
        <li>you'll get a report detailing the errors, if any.</li>
      </ol>
    </form>
"""


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



@app.route('/static/<path:filename>')
def send_foo(filename):
    return send_from_directory(STATIC_FOLDER, filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # global jobid
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            snap_tolerance = verify_snap_tolerance(request.form['snap_tolerance'])
            c.execute("INSERT INTO jobs VALUES ('%s', %f, '%s', %f)" % (fname, time.time(), '-', snap_tolerance))
            conn.commit()
            c.execute("SELECT rowid, timestamp FROM jobs where fname='%s' ORDER BY timestamp DESC" % fname)
            jid = c.fetchone()[0]
            s = "<h2>done.</h2>"
            s += "<p>The id for your validation task is %d.</p>" % jid
            s += "<p>The validation report will soon be available <a href='/reports/%d'>there</a>; it might take a few minutes, depending on the size of the file.</p>" % jid
            return wwwheader + s + wwwfooter
        else:
          return wwwheader + "<h2>ERROR</h2><p>File not of GML/XML type</p>" + wwwfooter
    r = wwwheader + wwwindex + wwwfooter
    return r


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/errors')
def errors():
    return wwwheader + wwwerrors + wwwfooter

@app.route('/about')
def about():
    i = open('about.html')
    return wwwheader + i.read() + wwwfooter

@app.route('/contact')
def contact():
    i = open('contact.html')
    return wwwheader + i.read() + wwwfooter


@app.route('/faq')
def faq():
    i = open('faq.html')
    return wwwheader + i.read() + wwwfooter

@app.route('/reports/download/<int:jobid>')
def download_report(jobid):
    # report = REPORTS_FOLDER + 'report%d.xml' % jobid
    return send_from_directory(app.config['REPORTS_FOLDER'], 'report%d.xml' % jobid)


@app.route('/reports/<int:jobid>')
def show_post(jobid):
    c.execute("SELECT fname, report FROM jobs where rowid='%d'" % jobid)
    report = c.fetchone()
    if (report == None) or (report[1] == '-'):
      s = "<h3>Error: no such report or the process is not finished.<br><br> Be patient.</h3>"
      return wwwheader + s + wwwfooter
    else:
      summary = report[1].split('\n')
      print summary
      s = '<h2>Report for file %s</h2>' % report[0]
      s += '<p>%s</p>' % summary[0]
      s += '<p>%s</p>' % summary[1]
      if (summary[2] == 'Hourrraaa!'):
        if (summary[0] != 'Number of solids in file: 0'):
          s += '<img src="/static/welldone.png" width="120" alt="">'
      else:
        s += "<p>%s (<a href='/errors'>overview of the possible errors</a>)</p><ol>" % summary[2]
        for er in summary[3:]:
          s += '<il>%s</il>' % er
      s += "</ol>"
      s += "<p><a href='/reports/download/%d'>report%d.xml</a></p>" % (jobid, jobid)
      return wwwheader + s + wwwfooter

if __name__ == '__main__':
    app.run(debug=True) # TODO: no debug in release mode!



