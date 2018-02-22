
import os
import sys
import shutil
import glob
import subprocess
import json
from StringIO import StringIO


def validate(jid, 
             fin, 
             snap_tol, 
             planarity_d2p_tol, 
             overlap_tol, 
             prim3d, 
             ignore204, 
             geom_is_sem_surfaces, 
             val3dityexefolder, 
             reportsfolder):
  cmd = []
  cmd.append(val3dityexefolder + "val3dity")
  cmd.append(fin)
  cmd.append("--snap_tol")
  cmd.append(str(snap_tol))
  cmd.append("--planarity_d2p_tol")
  cmd.append(str(planarity_d2p_tol))
  cmd.append("--overlap_tol")
  cmd.append(str(overlap_tol))
  cmd.append("-p")
  cmd.append(prim3d)
  if (ignore204 == True):
    cmd.append("--ignore204")
  if (geom_is_sem_surfaces == True):
    cmd.append("--geom_is_sem_surfaces")
  cmd.append("--report_json")
  finfull = reportsfolder + jid + ".json"
  cmd.append(finfull)
  print " ".join(cmd)
  op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  R = op.poll()
  if R:
    res = op.communicate()
    raise ValueError(res[1])
  re =  op.communicate()[0]
  #-- read json report
  j = json.loads(open(finfull).read())
  
  dSummary = {}
  dSummary['total_features'] = j["total_features"]
  dSummary['invalid_features'] = j["invalid_features"]
  dSummary['total_primitives'] = j["total_primitives"]
  dSummary['invalid_primitives'] = j["invalid_primitives"]
  if (j["overview_errors"] == None):
    dSummary['errors'] = "-1"
  else:
    dSummary['errors'] = "-".join(map(str, j["overview_errors"]))
  return dSummary


if __name__ == '__main__':
  r = validate("myjid", 
               "/Users/hugo/data/val3dity/Munchen/LOD2_4424_5482_solid.gml", 
               # "/Users/hugo/projects/val3dity/data/cityjson/cube.json", 
               # "/Users/hugo/projects/val3dity/data/poly/cube5.off", 
               "0.001",
               "0.01", 
               "-1", 
               "Solid",
               False,
               False,
               "/Users/hugo/projects/val3dity/build/",
               "/Users/hugo/temp/reports/")
  print r
