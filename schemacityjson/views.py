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
    bValid, woWarnings, errors, warnings = cm.validate()

    print(bValid)
    return True
    # doc, xsd = getXML(fIn, folder)
    # if (doc == None) and (xsd == None):
    #     return "Invalid CityGML document: not a CityGML document."
    # xmlschema = etree.XMLSchema(xsd)
    # valid = doc.xmlschema(xsd)
    # if valid == True:
    #     return True
    # else:
    #     try:
    #         xmlschema.assert_(doc)
    #     except AssertionError as e:
    #         return str(e)




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
                re = validateonefile(app.config['UPLOAD_FOLDER']+fname, app.config['SCHEMAROOT'])
                os.remove(app.config['UPLOAD_FOLDER']+fname)
                if re == True:
                    return render_template("index.html", valid=True, fname=fname)           
                else:
                    return render_template("index.html", valid=True, error=re, fname=fname)           
            else:
                return render_template("index.html", problem='Uploaded file is not a JSON file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html")





