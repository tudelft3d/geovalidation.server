import sys
import os
import glob
from lxml import etree


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


