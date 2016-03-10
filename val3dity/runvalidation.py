
import os
import sys
import shutil
import glob
import subprocess
from lxml import etree
from StringIO import StringIO


def validate(jid, fin, primitives, snaptol, plantol, val3dityexefolder, reportsfolder):
  cmd = []
  cmd.append(val3dityexefolder + "val3dity")
  cmd.append(fin)
  cmd.append("-p")
  cmd.append(primitives)
  cmd.append("--oxml")
  cmd.append(reportsfolder + jid + ".xml")
  cmd.append("--planarity_d2p")
  cmd.append(str(plantol))
  cmd.append("--snap_tolerance")
  cmd.append(str(snaptol))
  cmd.append("--unittests")
  # print " ".join(cmd)
  op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  R = op.poll()
  if R:
    res = op.communicate()
    raise ValueError(res[1])
  re =  op.communicate()[0]
  # print re
  dSummary = {}
  dSummary['noprimitives'] = 0
  dSummary['noinvalid'] = 0
  dSummary['errors'] = 901
  output = []
  if (re != ''):
      if (re.find('@VALID') != -1):
        print "VALID"
        return output
      i = re.find('@INVALID')
      s = re[i+9:]
      tmp = s.split(" ")
      codes = map(int, tmp[:-1])
      for each in codes:
        if output.count(each) == 0:
          output.append(each)
      print codes
  return output




def validate2(jid, fin, primitives, snaptol, plantol, uploadtime, val3dityexefolder, tmpfolder):
  fin = open(fin)
  if (construct_polys(jid, fin, primitives, snaptol, val3dityexefolder, tmpfolder) == 1):
    reportxml, dSummary = validate_polys(jid, fin, primitives, snaptol, plantol, uploadtime, val3dityexefolder, tmpfolder)
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


def construct_polys(jid, fin, primitives, snap, val3dityexe_folder, tmpfolder):
  print "Extracting the 3D primitives from the CityGML file"
  print fin.name
  GML2POLYEXE = 'python %sressources/python/gml2poly/gml2poly.py' % (val3dityexe_folder)
  TMPOLYS_FOLDER = tmpfolder + jid
  print "temp folder:", TMPOLYS_FOLDER
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


def validate_polys(jid, fin, primitives, snap, planarity, uploadtime, val3dityexefolder, tmpfolder):
  dSummary = {}
  dFiles = {}
  TMPOLYS_FOLDER = tmpfolder + jid
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
    cmd.append(val3dityexefolder + "val3dity")
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
  validate("myjid", 
           "/Users/hugo/data/val3dity/Munchen/LOD2_4424_5482_solid.gml", 
           "S", 
           "0.001", 
           "0.01", 
           "/Users/hugo/projects/val3dity/",
           "/Users/hugo/temp/reports/")
