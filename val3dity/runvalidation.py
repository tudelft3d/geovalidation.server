
import os
import sys
import shutil
import glob
import subprocess
from lxml import etree
from StringIO import StringIO

VAL3DITYEXE_FOLDER = '/Users/hugo/projects/val3dity/'
# VAL3DITYEXE_FOLDER = '/Users/roger'
TMP_FOLDER      = '/tmp/'

# if VAL3DITYEXE_FOLDER in os.environ:
#   VAL3DITYEXE_FOLDER = os.environ['VAL3DITYEXE_FOLDER']
# if TMP_FOLDER   in os.environ:
#   TMP_FOLDER = os.environ['TMP_FOLDER']

# print VAL3DITYEXE_FOLDER
# # print os.environ
# if 'GEOVALIDATION_SETTINGS' in os.environ:
#   print os.environ['GEOVALIDATION_SETTINGS']
# GML2POLYEXE    = 'python %sressources/python/gml2poly/gml2poly.py' % (VAL3DITYEXE_FOLDER)
# TMPOLYS_FOLDER = TMP_FOLDER + 'tmpolys/'


def validate(fin, primitives, snaptol, plantol, uploadtime):
  fin = open(fin)
  if (construct_polys(fin, primitives, snaptol) == 1):
    reportxml, dSummary = validate_polys(fin, primitives, snaptol, plantol, uploadtime)
  else: #-- something went wrong, XML probably invalid
    reportxml = []
    reportxml.append('<val3dity>')
    a = (fin.name).rfind('/')
    reportxml.append('\t<inputFile>' + (fin.name)[a+1:] + '</inputFile>')
    if (primitives == 'ms'):
      reportxml.append('\t<primitives>' + 'gml:MultiSurface' + '</primitives>')
    else:
      reportxml.append('\t<primitives>' + 'gml:Solid' + '</primitives>')
    reportxml.append('\t<snaptolerance>' + str(snaptol) + '</snaptolerance>')
    reportxml.append('\t<planaritytolerance>' + str(plantol) + '</planaritytolerance>')
    reportxml.append('\t<time>' + str(uploadtime) + '</time>')
    reportxml.append("ERROR: Problems with parsing the XML. Cannot validate.")
    reportxml.append('</val3dity>')
    dSummary = {}
    dSummary['noprimitives'] = 0
    dSummary['noinvalid'] = 0
    dSummary['errors'] = 901
  return reportxml, dSummary


def construct_polys(fin, primitives, snap):
  print "Extracting the 3D primitives from the CityGML file"
  print fin.name
  if not os.path.exists(TMPOLYS_FOLDER):
      os.mkdir(TMPOLYS_FOLDER)
  else:
      shutil.rmtree(TMPOLYS_FOLDER)
      os.mkdir(TMPOLYS_FOLDER)
  if primitives == 'solid':
    s = "%s %s %s --snap_tolerance %s" % (GML2POLYEXE, fin.name, TMPOLYS_FOLDER, snap)
  else:
    s = "%s %s %s --multisurface --snap_tolerance %s" % (GML2POLYEXE, fin.name, TMPOLYS_FOLDER, snap)
  os.system(s)
  polys = os.listdir(TMPOLYS_FOLDER)
  if len(polys) == 1 and polys[0] == 'error': 
    return 0
  else:
    return 1


def validate_polys(fin, primitives, snap, planarity, uploadtime):
  dSummary = {}
  dFiles = {}
  os.chdir(TMPOLYS_FOLDER)
  for f in os.listdir('.'):
    if f[-4:] == 'poly':
      i = (f.split('.poly')[0]).rfind('.')
      f1 = f[:i]
      if f1 not in dFiles:
        dFiles[f1] = [f]
      else:
        dFiles[f1].append(f)
  i = 0
  dSummary['noprimitives'] = len(dFiles)
  invalidsolids = 0
  xmlsolids = []
  errorspresent = []
  for solidname in dFiles:
    cmd = []
    cmd.append(VAL3DITYEXE_FOLDER + "val3dity")
    if (primitives == 'ms'):
      cmd.append("-onlysurfaces")
    cmd.append("-xml")
    cmd.append("-planarity_d2p")
    cmd.append(str(planarity))
    for s in dFiles[solidname]:
      cmd.append(s)
    op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                          
    R = op.poll()
    if R:
      res = op.communicate()
      raise ValueError(res[1])
    o =  op.communicate()[0]
    if o.find('ERROR') != -1:
      invalidsolids += 1
      i = o.find('<errorCode>')
      while (i != -1):
        if errorspresent.count(o[i+11:i+14]) == 0:
          errorspresent.append(o[i+11:i+14])
        tmp = o[i+1:].find('<errorCode>')
        if tmp == -1:
          i = -1
        else:
          i = tmp + i + 1
      if primitives == 'solid':
        o = '\t<Solid>\n\t\t<id>' + solidname + '</id>\n' + o + '\t</Solid>'
      else:
        o = '\t<MultiSurface>\n\t\t<id>' + solidname + '</id>\n' + o + '\t</MultiSurface>'
      xmlsolids.append(o)
    
  reportxml = []
  reportxml.append('<val3dity>')
  a = (fin.name).rfind('/')
  reportxml.append('\t<inputFile>' + (fin.name)[a+1:] + '</inputFile>')
  if (primitives == 'ms'):
    reportxml.append('\t<primitives>' + 'gml:MultiSurface' + '</primitives>')
  else:
    reportxml.append('\t<primitives>' + 'gml:Solid' + '</primitives>')
  reportxml.append('\t<snaptolerance>' + str(snap) + '</snaptolerance>')
  reportxml.append('\t<planaritytolerance>' + str(planarity) + '</planaritytolerance>')
  reportxml.append('\t<time>' + uploadtime + '</time>')
  reportxml.append("\n".join(xmlsolids))
  reportxml.append('</val3dity>')
  
  dSummary['noinvalid'] = invalidsolids
  if len(errorspresent) == 0:
    dSummary['errors'] = "-1"
  else:
    dSummary['errors'] = "-".join(errorspresent)
  return reportxml, dSummary

if __name__ == '__main__':
  validate(sys.argv[1], "solid", "0.001", "0.001", "2015-02-13")
