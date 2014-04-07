from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER      = './uploads'
REPORTS            = './reports'
ALLOWED_EXTENSIONS = set(['gml', 'xml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


jobid = 1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return 'Hello World!'
    # return app.send_static_file('index.html')
    # return send_from_directory('/Users/hugo/Dropbox/temp/flask', 'index.html')


@app.route('/test1')
def test1():
    s = "your are at: " + os.getcwd()
    return s

@app.route('/reports/<int:pid>')
def show_post(pid):
    # show the post with the given id, the id is an integer
    # return 'Report%d.xml' % pid
    return send_from_directory('/Users/hugo/temp', 'report133.xml')



@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    global jobid
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            # return redirect(url_for('uploaded_file', filename=fname))
            s = "File %s will be validated and your report available at localhost:5000/reports/%d" % (fname, jobid)
            jobid += 1
            # hugo(fname)
            return s
        else:
          return "File not of GML/XML type"
    return '''
    <!doctype html>
    <title>Upload your citygml file</title>
    <h1>Upload your citygml file</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    app.run(debug=True)
