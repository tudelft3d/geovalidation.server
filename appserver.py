from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pickle
import time
import val3dity

UPLOAD_FOLDER      = '/Users/hugo/www/geovalidation/uploads/'
REPORTS_FOLDER     = '/Users/hugo/www/geovalidation/reports/'
ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER

try:
    inputjobs = open('alljobs.pkl', 'rb')
    ALLJOBS = pickle.load(inputjobs)
except IOError:
    ALLJOBS = []



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def validate(jobid):
    fname = ALLJOBS[jobid][0]
    totalxml = val3dity.validate(UPLOAD_FOLDER+fname)
    s = REPORTS_FOLDER + str(jobid) + ".xml"
    fout = open(s, 'w')
    fout.write('\n'.join(totalxml))
    fout.close()


    #-- save to file the updated list with all jobs
    # job = ALLJOBS[jobid]
    # job.append(time.gmtime())
    # output = open('alljobs.pkl', 'wb')
    # pickle.dump(ALLJOBS, output)





# @app.route('/')
# def index():
#     return 'Hello World!'
#     # return app.send_static_file('index.html')
#     # return send_from_directory('/Users/hugo/Dropbox/temp/flask', 'index.html')

@app.route('/static/<path:filename>')
def send_foo(filename):
    return send_from_directory('/Users/hugo/www/geovalidation/static', filename)



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
            s = "The id for your validation task is %d.\n\n" % jid
            s += "When finished, the report will be at localhost:5000/reports/%d" % jid
            return s
        else:
          return "File not of GML/XML type."
    f = open('index.html', 'r')
    return f.read()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/reports/<int:jobid>')
def show_post(jobid):
    report = REPORTS_FOLDER+ '%d.xml' % jobid
    return send_from_directory(app.config['REPORTS_FOLDER'], '%d.xml' % jobid)


if __name__ == '__main__':
    app.run(debug=True)
