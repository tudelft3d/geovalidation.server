from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pickle
import time
import val3dity

ROOT_FOLDER        = '/Users/hugo/www/geovalidation/'
UPLOAD_FOLDER      = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER     = ROOT_FOLDER + 'reports/'
STATIC_FOLDER      = ROOT_FOLDER + 'static/'
ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER

try:
    inputjobs = open('alljobs.pkl', 'rb')
    ALLJOBS = pickle.load(inputjobs)
except IOError:
    ALLJOBS = []

wwwheader = """
<html>
  <head>
    <link href='http://fonts.googleapis.com/css?family=Inconsolata' rel='stylesheet' type='text/css'>
    <style>
      body {
        font-family: 'Inconsolata', null;
        font-size: 18px;
        background-color: #f4f4f4;
        font-color: #2df5dd;
        padding-top: 50px;
        /*width: 600px;*/
        text-align: center;
      }
      #wrapper{
        width:600px;
        margin:0 auto;
        text-align:left;
        /*padding-bottom: 50px;*/
      }
      #footer{
        margin:0 auto;
        width:600px;
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
  <form action="" method=post enctype=multipart/form-data>
  <h2>Geometric validation of solids according to the international standard ISO 19107</h2>
  <ol>
    <li><input type=file name=file> Choose your CityGML file containing one or more buildings </li>
    <li><input type=submit value=Upload> it to our server. We promise to delete it right after having validated it.</li>
    <li>You will be redirected to a page containing a report. This might take a few minutes, depending on the size of your file. </li>
    <li>If something doesn&#8217;t run as it should, please contact <a href="&#x6d;&#97;&#105;&#x6c;&#x74;&#111;&#58;&#104;&#46;&#x6c;&#101;&#100;&#x6f;&#x75;&#x78;&#64;&#x74;&#117;&#x64;&#x65;&#108;&#102;&#x74;&#x2e;&#x6e;&#x6c;">&#x6d;&#101;</a>.</li>
  </ol>
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def validate(jobid):
    job = ALLJOBS[jobid]
    fname = job[0]
    totalxml, summary = val3dity.validate(UPLOAD_FOLDER+fname)
    s = REPORTS_FOLDER + str(jobid) + ".xml"
    fout = open(s, 'w')
    fout.write('\n'.join(totalxml))
    fout.close()
    job.append(summary)
    #-- save to file the updated list with all jobs
    outname = ROOT_FOLDER + 'alljobs.pkl'
    print "pickle", outname
    output = open(outname, 'wb')
    pickle.dump(ALLJOBS, output)

@app.route('/hugo')
def hugo():
  r = wwwheader + "<h2>Potatoes</h2>" + wwwfooter
  return r

@app.route('/static/<path:filename>')
def send_foo(filename):
    return send_from_directory(STATIC_FOLDER, filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global jobid
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # return redirect(url_for('uploaded_file', filename=fname))
            jid = len(ALLJOBS)
            ALLJOBS.append([fname, time.gmtime()])
            validate(jid)
            s = "<h2>done.</h2>"
            s += "<p>The id for your validation task is %d.</p>" % jid
            s += "<p>The validation report will be available <a href='/reports/%d'>there</a> soon; it might take a few minutes, be patient.</p>" % jid
            return wwwheader + s + wwwfooter
        else:
          return wwwheader + "<h2>ERROR</h2><p>File not of GML/XML type</p>" + wwwfooter
    r = wwwheader + wwwindex + wwwfooter
    return r


# TODO: remove that
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/reports/download/<int:jobid>')
def download_report(jobid):
    report = REPORTS_FOLDER+ '%d.xml' % jobid
    return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)


@app.route('/reports/<int:jobid>')
def show_post(jobid):
    if (jobid >= len(ALLJOBS)):
      return "Error: no such report"
    else:
      job = ALLJOBS[jobid]
      summary = job[2].split('\n')
      print summary
      s = '<h2>Report for file %s</h2>' % job[0]
      for l in summary:
        s += '<p>%s</p>' % l
      s += "<p><a href='/reports/download/%d'>Download the report</a></p>" % jobid
      return wwwheader + s + wwwfooter
    # report = REPORTS_FOLDER+ '%d.xml' % jobid
    # return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)


if __name__ == '__main__':
    app.run(debug=True) # TODO: no debug in release mode!
