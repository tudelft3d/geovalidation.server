
ROOT_FOLDER        = '/Users/hugo/www/geovalidation/val3dity/'
VAL3DITY_FOLDER    = '/Users/hugo/projects/val3dity/'
TMPOLYS_FOLDER     = '/Users/hugo/temp/tmpolys/'

# ROOT_FOLDER        = '/var/www/geovalidation/val3dity/'
# VAL3DITY_FOLDER    = '/home/hledoux/projects/val3dity/'
# TMPOLYS_FOLDER     = '/home/hledoux/temp/tmpolys/'

DATABASE            = ROOT_FOLDER + 'val3dity.sqlite'
UPLOAD_FOLDER       = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER      = ROOT_FOLDER + 'reports/'
PROBLEMFILES_FOLDER = ROOT_FOLDER + 'problemfiles/'
TMP_FOLDER          = ROOT_FOLDER + 'tmp/'
STATIC_FOLDER       = ROOT_FOLDER + 'static/'
ADDGMLIDS_EXE       = 'python %sressources/python/addgmlids.py' % (VAL3DITY_FOLDER)
GML2POLY_EXE        = 'python %sressources/python/gml2poly/gml2poly.py' % (VAL3DITY_FOLDER)
