from schemacityjson import app

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from cjio import cityjson



ALLOWED_EXTENSIONS = set(['json'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def validateonefile(fIn, folder):
    cj_file = open(fIn, 'r')
    cm = cityjson.reader(file=cj_file)
    return cm.validate()

    
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            if allowed_file(f.filename):
                fname = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                bValid, woWarnings, errors, warnings = validateonefile(app.config['UPLOAD_FOLDER']+fname, app.config['CJSCHEMAROOT'])
                os.remove(app.config['UPLOAD_FOLDER']+fname)
                if bValid == True:
                    return render_template("index.html", valid=1, warnings=warnings, fname=fname)           
                else:
                    return render_template("index.html", valid=-1, errors=errors, warnings=warnings, fname=fname)           
            else:
                return render_template("index.html", valid=-1, errors=['Uploaded file is not a JSON file.'])
        else:
            return render_template("index.html", valid=0, errors=['No file selected.'])
    return render_template("index.html")





