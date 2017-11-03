
import os
import sys
import shutil
import glob
import subprocess
from lxml import etree
from StringIO import StringIO


def validate(jid, fin, primitives, snaptol, plantol, usebuildings, val3dityexefolder, reportsfolder):
  cmd = []
  cmd.append(val3dityexefolder + "val3dity")
  cmd.append(fin)
  cmd.append("-p")
  cmd.append(primitives)
  cmd.append("-r")
  cmd.append(reportsfolder + jid + ".xml")
  cmd.append("--planarity_d2p")
  cmd.append(str(plantol))
  cmd.append("--snap_tolerance")
  cmd.append(str(snaptol))
  cmd.append("--unittests")
  if usebuildings == 1:
    cmd.append("-B")
  print " ".join(cmd)
  op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  R = op.poll()
  if R:
    res = op.communicate()
    raise ValueError(res[1])
  re =  op.communicate()[0]
  dSummary = {}
  if (re != ''):
      if (re.find('@VALID') != -1):
        i = re.find('@VALID')
        s = re[i+7:]
        codes = s.split(" ")
        dSummary['noprimitives'] = codes[0]
        dSummary['noinvalid'] = "0"
        dSummary['nobuildings'] = codes[2]
        dSummary['invalidbuildings'] = codes[3]
        dSummary['errors'] = "-1"
        return dSummary
      elif (re.find('@INVALID') != -1):
        i = re.find('@INVALID')
        s = re[i+9:]
        codes = s.split(" ")
        dSummary['noprimitives'] = codes[0]
        dSummary['noinvalid'] = codes[1]
        dSummary['nobuildings'] = codes[2]
        dSummary['invalidbuildings'] = codes[3]
        dSummary['errors'] = "-".join(codes[4:-1])
        return dSummary
      else:
        dSummary['noprimitives'] = 0
        dSummary['noinvalid'] = 0
        dSummary['nobuildings'] = 0
        dSummary['invalidbuildings'] = 0
        dSummary['errors'] = "999"
        return dSummary
  return dSummary


if __name__ == '__main__':
  r = validate("myjid", 
               "/Users/hugo/data/val3dity/Munchen/LOD2_4424_5482_solid.gml", 
               # "/Users/hugo/projects/val3dity/data/poly/cube.poly", 
               "S", 
               "0.001", 
               "0.01", 
               "/Users/hugo/projects/val3dity/",
               "/Users/hugo/temp/reports/")
  print r
