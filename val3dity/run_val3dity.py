import os
import sys
import shutil
import glob
import subprocess
from lxml import etree
from StringIO import StringIO

LOCAL = True

if LOCAL == True:
  VAL3DITY_FOLDER    = '/Users/hugo/projects/val3dity'
  TMPOLYS_FOLDER     = '/Users/hugo/temp/tmpolys'
  ROOT_FOLDER        = '/Users/hugo/www/geovalidation/val3dity/'
else:
  VAL3DITY_FOLDER    = '/home/hledoux/projects/val3dity'
  TMPOLYS_FOLDER     = '/home/hledoux/temp/tmpolys'
  ROOT_FOLDER        = '/var/www/geovalidation/'

UPLOAD_FOLDER      = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER     = ROOT_FOLDER + 'reports/'

dErrors = {
  100: 'REPEATED_POINTS',
  110: 'RING_NOT_CLOSED',   
  120: 'RING_SELF_INTERSECT',
  200: 'SELF_INTERSECTION',  
  210: 'NON_PLANAR_SURFACE',                     
  220: 'INTERIOR_DISCONNECTED',
  230: 'HOLE_OUTSIDE',
  240: 'HOLES_ARE_NESTED',                      
  250: 'ORIENTATION_RINGS_SAME',
  300: 'NOT_VALID_2_MANIFOLD',
  301: 'SURFACE_NOT_CLOSED',                     
  302: 'DANGLING_FACES',                         
  303: 'FACE_ORIENTATION_INCORRECT_EDGE_USAGE',  
  304: 'FREE_FACES',                             
  305: 'SURFACE_SELF_INTERSECTS',  
  306: 'VERTICES_NOT_USED',              
  310: 'SURFACE_NORMALS_WRONG_ORIENTATION',      
  400: 'SHELLS_FACE_ADJACENT',                   
  410: 'SHELL_INTERIOR_INTERSECT',               
  420: 'INNER_SHELL_OUTSIDE_OUTER',              
  430: 'INTERIOR_OF_SHELL_NOT_CONNECTED', 
}


def main():
    os.chdir(UPLOAD_FOLDER)
    jobs = glob.glob('*.txt')
    print jobs
    files = []
    for job in jobs:
        os.chdir(UPLOAD_FOLDER)
        details = open(job, 'r')
        jobid = job[:-4]
        fname = details.readline().rstrip('\n')
        files.append(fname)
        snap = details.readline().rstrip('\n')
        time = details.readline().rstrip('\n')
        totalxml, summary = validate(UPLOAD_FOLDER+fname, snap, time)
        print "validation finished."
        s = "%s%s.xml" % (REPORTS_FOLDER, jobid)        
        fout = open(s, 'w')
        fout.write('\n'.join(totalxml))
        fout.close()
        s = "%s%s.txt" % (REPORTS_FOLDER, jobid)        
        fout = open(s, 'w')
        fout.write(summary)
        fout.close()
    #-- remove all the files once validated
    for job in jobs:
        os.remove(UPLOAD_FOLDER+job)
    for fname in files:
        if os.path.exists(UPLOAD_FOLDER+fname):
            os.remove(UPLOAD_FOLDER+fname)


def validate(fin, snap, time):
  fin = open(fin)
  if (construct_polys(fin, snap) == 1):
    totalxml, summary = validate_polys(fin, snap, time)
    return totalxml, summary
  else:
    totalxml = []
    totalxml.append('<val3dity>')
    a = (fin.name).rfind('/')
    totalxml.append('\t<inputFile>' + (fin.name)[a+1:] + '</inputFile>')
    totalxml.append('\t<snaptolerance>' + snap + '</snaptolerance>')
    totalxml.append('\t<time>' + time + '</time>')
    totalxml.append("ERROR: Problems with parsing the XML. Cannot validate.")
    totalxml.append('</val3dity>')
    return totalxml, "ERROR: Problems with parsing the XML. Cannot validate."

def construct_polys(fin, snap):
  print "Extracting the solids from the CityGML file"
  if not os.path.exists(TMPOLYS_FOLDER):
      os.mkdir(TMPOLYS_FOLDER)
  else:
      shutil.rmtree(TMPOLYS_FOLDER)
      os.mkdir(TMPOLYS_FOLDER)
  s = "python %s/ressources/python/gml2poly/gml2poly.py %s %s --snap_tolerance %s" % (VAL3DITY_FOLDER, fin.name, TMPOLYS_FOLDER, snap)
  os.system(s)
  polys = os.listdir(TMPOLYS_FOLDER)
  if len(polys) == 1 and polys[0] == 'error': 
    return 0
  else:
    return 1

def remove_tmpolys():
  os.chdir("..")
  shutil.rmtree("tmpolys")


def validate_polys(fin, snap, time):
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
  summary += "Number of solids in file: %d\n" % (len(dFiles))
  invalidsolids = 0
  xmlsolids = []
  exampleerrors = []
  for solidname in dFiles:
    # validate with val3dity
    str1 = VAL3DITY_FOLDER + "/val3dity -xml " +  " ".join(dFiles[solidname])
    print str1
    op = subprocess.Popen(str1.split(' '),
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
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
      o = '\t<Solid>\n\t\t<id>' + solidname + '</id>\n' + o + '\t</Solid>'
      xmlsolids.append(o)
    
  totalxml = []
  totalxml.append('<val3dity>')
  a = (fin.name).rfind('/')
  totalxml.append('\t<inputFile>' + (fin.name)[a+1:] + '</inputFile>')
  totalxml.append('\t<snaptolerance>' + snap + '</snaptolerance>')
  totalxml.append('\t<time>' + time + '</time>')
  totalxml.append("\n".join(xmlsolids))
  totalxml.append('</val3dity>')
  
  summary += "Number of invalid solids: %d\n" % invalidsolids
  if (invalidsolids == 0):
    summary += "Hourrraaa!\n"
  else:
    summary += "Errors present:\n"
    for each in exampleerrors:
      summary += each + " " + str(dErrors[int(each)]) + "\n"
  return totalxml, summary

if __name__ == '__main__':
    main()