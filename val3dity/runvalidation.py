import os
import sys
import shutil
import glob
import subprocess
from lxml import etree
from StringIO import StringIO
from settings import *


dErrors = {
  101: 'TOO_FEW_POINTS',
  102: 'CONSECUTIVE_POINTS_SAME',
  103: 'RING_NOT_CLOSED',
  104: 'RING_SELF_INTERSECTION',
  105: 'RING_COLLAPSED',
  201: 'INTERSECTION_RINGS',
  202: 'DUPLICATED_RINGS',
  203: 'NON_PLANAR_POLYGON_DISTANCE_PLANE',
  204: 'NON_PLANAR_POLYGON_NORMALS_DEVIATION',
  205: 'POLYGON_INTERIOR_DISCONNECTED',
  206: 'HOLE_OUTSIDE',
  207: 'INNER_RINGS_NESTED',
  208: 'ORIENTATION_RINGS_SAME',
  300: 'NOT_VALID_2_MANIFOLD',
  301: 'TOO_FEW_POLYGONS',
  302: 'SHELL_NOT_CLOSED',
  303: 'NON_MANIFOLD_VERTEX',
  304: 'NON_MANIFOLD_EDGE',
  305: 'MULTIPLE_CONNECTED_COMPONENTS',
  306: 'SHELL_SELF_INTERSECTION',
  307: 'POLYGON_WRONG_ORIENTATION',
  308: 'ALL_POLYGONS_WRONG_ORIENTATION',
  309: 'VERTICES_NOT_USED',
  401: 'SHELLS_FACE_ADJACENT',
  402: 'INTERSECTION_SHELLS',
  403: 'INNER_SHELL_OUTSIDE_OUTER',
  404: 'SOLID_INTERIOR_DISCONNECTED',
}



def validate(fin, primitives, snap, planarity):
  fin = open(fin)
  if (construct_polys(fin, primitives, snap) == 1):
    totalxml, summary = validate_polys(fin, primitives, snap, planarity)
    return totalxml, summary
  else: #-- something went wrong, XML probably invalid
    totalxml = []
    totalxml.append('<val3dity>')
    a = (fin.name).rfind('/')
    totalxml.append('\t<inputFile>' + (fin.name)[a+1:] + '</inputFile>')
    totalxml.append('\t<snaptolerance>' + snap + '</snaptolerance>')
    totalxml.append("ERROR: Problems with parsing the XML. Cannot validate.")
    totalxml.append('</val3dity>')
    return totalxml, "ERROR: Problems with parsing the XML. Cannot validate."


def construct_polys(fin, primitives, snap):
  print "Extracting the 3D primitives from the CityGML file"
  if not os.path.exists(TMPOLYS_FOLDER):
      os.mkdir(TMPOLYS_FOLDER)
  else:
      shutil.rmtree(TMPOLYS_FOLDER)
      os.mkdir(TMPOLYS_FOLDER)
  if primitives == 'solid':
    s = "%s %s %s --snap_tolerance %s" % (GML2POLY_EXE, fin.name, TMPOLYS_FOLDER, snap)
  else:
    s = "%s %s %s --multisurface --snap_tolerance %s" % (GML2POLY_EXE, fin.name, TMPOLYS_FOLDER, snap)
  os.system(s)
  polys = os.listdir(TMPOLYS_FOLDER)
  if len(polys) == 1 and polys[0] == 'error': 
    return 0
  else:
    return 1

def remove_tmpolys():
  os.chdir("..")
  shutil.rmtree("tmpolys")


def validate_polys(fin, primitives, snap, planarity):
  summary = ""
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
  summary += "Number of primitives in file: %d\n" % (len(dFiles))
  invalidsolids = 0
  xmlsolids = []
  exampleerrors = []
  for solidname in dFiles:
    cmd = []
    cmd.append(VAL3DITY_FOLDER + "val3dity")
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
        if exampleerrors.count(o[i+11:i+14]) == 0:
          exampleerrors.append(o[i+11:i+14])
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
    
  totalxml = []
  totalxml.append('<val3dity>')
  a = (fin.name).rfind('/')
  totalxml.append('\t<inputFile>' + (fin.name)[a+1:] + '</inputFile>')
  if (primitives == 'ms'):
    totalxml.append('\t<primitives>' + 'gml:MultiSurface' + '</primitives>')
  else:
    totalxml.append('\t<primitives>' + 'gml:Solid' + '</primitives>')
  totalxml.append('\t<snaptolerance>' + snap + '</snaptolerance>')
  totalxml.append('\t<planaritytolerance>' + planarity + '</planaritytolerance>')
  totalxml.append("\n".join(xmlsolids))
  totalxml.append('</val3dity>')
  
  summary += "Number of invalid primitives: %d\n" % invalidsolids
  if (invalidsolids == 0):
    summary += "Hourrraaa!\n"
  else:
    summary += "Errors present:\n"
    for each in exampleerrors:
      summary += each + " " + str(dErrors[int(each)]) + "\n"
  return totalxml, summary

# if __name__ == '__main__':
#     main()