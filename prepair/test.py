import os
import subprocess

cmd = []
cmd.append('/Users/hugo/projects/val3dity/val3dity')
# cmd.append('/Users/hugo/projects/prepair/prepair')
# cmd.append('ls')
# cmd.append("--help ")
# cmd.append("--wkt ")
# cmd.append("'POLYGON((0 0, 0 10, 10 0, 10 10, 0 0))'")
# wkt = "POLYGON((0 0, 0 10, 10 0, 10 10, 0 0))"
# cmd.append("'%s'" % wkt)
print cmd
op = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
R = op.poll()
if R:
  res = op.communicate()
  raise ValueError(res[1])
o =  op.communicate()[0]
print len(o)
print o