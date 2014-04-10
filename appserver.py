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

# try:
#     inputjobs = open('alljobs.pkl', 'rb')
#     ALLJOBS = pickle.load(inputjobs)
# except IOError:
#     ALLJOBS = []

conn = sqlite3.connect('alljobs.db', check_same_thread = False)
c = conn.cursor()
print "sqlite connected"


wwwheader = """
<html>
  <head>
    <link href='http://fonts.googleapis.com/css?family=Inconsolata' rel='stylesheet' type='text/css'>
    <style>
      body {
        font-family: 'Inconsolata', null;
        font-size: 18px;
        background-color: #fafafa;
        font-color: #2df5dd;
        padding-top: 50px;
        text-align: center;
      }
      #wrapper{
        width: 700px;
        margin: 0 auto;
        text-align: left;
        /*padding-bottom: 50px;*/
      }
      #footer{
        margin: 0 auto;
        width: 700px;
        padding-top: 20px;
        padding-bottom: 5px;
        text-align: center;
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
      <a href="http://www.tudelft.nl"><img src="/static/tudlogo.png" height="30" alt=""></a>
    </div>
  </body>
</html>
"""

wwwindex = """
  <title>val3dity: geometric validation of solids according to ISO19107</title>
  <h2>Geometric validation of solids according to the international standard ISO 19107</h2>
  <ol>
    <li>Choose your CityGML file containing one or more buildings. </li>
    <li>Upload it to our server. We promise to delete it right after having validated it.</li>
    <li>You will be redirected to a page containing a report.</li>
    <li>If something doesn&#8217;t run as it should, please contact <a href="&#x6d;&#97;&#105;&#x6c;&#x74;&#111;&#58;&#104;&#46;&#x6c;&#101;&#100;&#x6f;&#x75;&#x78;&#64;&#x74;&#117;&#x64;&#x65;&#108;&#102;&#x74;&#x2e;&#x6e;&#x6c;">&#x6d;&#101;</a>.</li>
  </ol>
  <hr/>
  <form action="" method=post enctype=multipart/form-data>
    <input type=file name=file><br>
    <input type=submit value=Upload>
  </form>
  <hr/>
  <p>In the background, two open-source projects are used: <a href="https://github.com/tudelft-gist/val3dity">val3dity</a> is used for the geometric validation, and <a href="https://github.com/tudelft-gist/citygml2poly">citygml2poly</a> is used to parse CityGML files.</p>
  <p>The validation of a solid is performed hierarchically, ie first every surface is validated in 2D (with <a href="http://trac.osgeo.org/geos/">GEOS</a>), then every shell is validated (must be watertight, no self-intersections, orientation of the normals must be consistent and pointing outwards, etc), and finally the interactions between the shells are analysed (for solids having inner shells/cavities).</p>
  <p>Most of the details of the implementation are available in this scientific article:</p>
  <blockquote>
  <p>Ledoux, Hugo (2013). On the validation of solids represented with the
  international standards for geographic information. <em>Computer-Aided Civil and Infrastructure Engineering</em>, 28(9):693&#8211;706. <a href="http://homepage.tudelft.nl/23t4p/pdfs/_13cacaie.pdf"> [PDF] </a> <a href="http://dx.doi.org/10.1111/mice.12043"> [DOI] </a></p>
  </blockquote>
"""

# return app.send_static_file('index.html')
# return send_from_directory('/Users/hugo/Dropbox/temp/flask', 'index.html')
# return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)
# return redirect(url_for('uploaded_file', filename=fname))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/hugo')
def hugo():
  r = wwwheader + "<h2>Potatoes</h2>" + wwwfooter
  return r

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
            c.execute("INSERT INTO jobs VALUES ('%s', %f, '%s')" % (fname, time.time(), '-'))
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


@app.route('/reports/download/<int:jobid>')
def download_report(jobid):
    # report = REPORTS_FOLDER + 'report%d.xml' % jobid
    return send_from_directory(app.config['REPORTS_FOLDER'], 'report%d.xml' % jobid)


@app.route('/reports/<int:jobid>')
def show_post(jobid):
    c.execute("SELECT fname, report FROM jobs where rowid='%d'" % jobid)
    report = c.fetchone()
    if (report == None) or (report[1] == '-'):
      s = "<h2>Error: no such report or the process is not finished. Be patient.</h2>"
      return wwwheader + s + wwwfooter
    else:
      summary = report[1].split('\n')
      print summary
      s = '<h2>Report for file %s</h2>' % report[0]
      s += '<p>%s</p>' % summary[0]
      s += '<p>%s</p>' % summary[1]
      if summary[2] == 'Hourrraaa!':
        s += '<p>%s</p>' % summary[2]
      else:
        s += '<p>%s</p><ol>' % summary[2]
        for er in summary[3:]:
          s += '<il>%s</il>' % er
      s += "</ol>"
      s += "<p><a href='/reports/download/%d'>report%d.xml</a></p>" % (jobid, jobid)
      return wwwheader + s + wwwfooter

if __name__ == '__main__':
    app.run(debug=True) # TODO: no debug in release mode!



