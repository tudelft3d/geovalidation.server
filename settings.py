DEBUG                 = False

PREPAIREXE            = '/Users/hugo/projects/prepair/prepair'
ROOT_FOLDER           = '/Users/hugo/www/geovalidation/prepair/'
STATIC_FOLDER         = ROOT_FOLDER + 'static/'

ROOT_FOLDER           = '/Users/hugo/www/geovalidation/val3dity/'
DATABASE              = ROOT_FOLDER + 'val3dity.sqlite'
UPLOAD_FOLDER         = ROOT_FOLDER + 'uploads/'
REPORTS_FOLDER        = ROOT_FOLDER + 'reports/'
PROBLEMFILES_FOLDER   = ROOT_FOLDER + 'problemfiles/'
STATIC_FOLDER         = ROOT_FOLDER + 'static/'
  
TMP_FOLDER            = '/tmp/'

VAL3DITY_FOLDER       = '/Users/hugo/projects/val3dity/'
ADDGMLIDS_EXE         = 'python %sressources/python/addgmlids.py' % (VAL3DITY_FOLDER)
GML2POLY_EXE          = 'python %sressources/python/gml2poly/gml2poly.py' % (VAL3DITY_FOLDER)
  
CELERY_BROKER_URL     = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

