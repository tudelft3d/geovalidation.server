from schemacitygml import app

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

import valxsdcitygml

ALLOWED_EXTENSIONS = set(['gml', 'xml'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
                re = valxsdcitygml.validateonefile(app.config['UPLOAD_FOLDER']+fname, app.config['SCHEMAROOT'])
                os.remove(app.config['UPLOAD_FOLDER']+fname)
                if re == True:
                    return render_template("index.html", valid=True, fname=fname)           
                else:
                    return render_template("index.html", valid=True, error=re, fname=fname)           
            else:
                return render_template("index.html", problem='Uploaded file is not a XML/GML file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html")





