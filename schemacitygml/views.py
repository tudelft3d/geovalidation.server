from schemacitygml import app

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from lxml import etree



ALLOWED_EXTENSIONS = set(['gml', 'xml'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def validateonefile(fIn, folder):
    doc, xsd = getXML(fIn, folder)
    if (doc == None) and (xsd == None):
        return "Invalid CityGML document: not a CityGML document."
    xmlschema = etree.XMLSchema(xsd)
    valid = doc.xmlschema(xsd)
    if valid == True:
        return True
    else:
        try:
            xmlschema.assert_(doc)
        except AssertionError as e:
            return str(e)


def getXML(fIn, folder):
    parser = etree.XMLParser(ns_clean=True)
    try:
        doc = etree.parse(fIn)    
    except:
        doc = None
        xsd = None
        return doc, xsd
    root = doc.getroot()
    citygmlversion = ""
    for key in root.nsmap.keys():
        if root.nsmap[key].find('www.opengis.net/citygml') != -1:
            if (root.nsmap[key][-3:] == '0.4'):
                citygmlversion = '0.4'
                break
            if (root.nsmap[key][-3:] == '1.0'):
                citygmlversion = '1.0'
                break
            if (root.nsmap[key][-3:] == '2.0'):
                citygmlversion = '2.0'
                break
    if citygmlversion == "":
        return None, None
    if citygmlversion == "0.4":
        xsd = etree.parse(folder + "schemas/v0.4/CityGML.xsd")
    elif citygmlversion == "1.0":
        xsd = etree.parse(folder + "schemas/v1.0/CityGML.xsd")
    else:
        xsd = etree.parse(folder + "schemas/v2.0/CityGML.xsd")
    return doc, xsd




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
                return render_template("index.html", problem='Uploaded file is not a XML/GML file.')
        else:
            return render_template("index.html", problem='No file selected.')
    return render_template("index.html")





