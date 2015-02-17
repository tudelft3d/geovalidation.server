from flask import Flask
from celery import Celery

# from settings import *

app = Flask(__name__, static_url_path='')

class default_settings(object):
    VAL3DITY_SERVER       = '/Users/hugo/www/geovalidation/val3dity/'
    VAL3DITYEXE_FOLDER    = '/Users/hugo/projects/val3dity/'
    TMP_FOLDER             = '/tmp/'
    CELERY_BROKER_URL      = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND  = 'redis://localhost:6379/0'

app.config.from_object(default_settings)
app.config.from_envvar('GEOVALIDATION_SETTINGS', silent=True)

#-- fixed setup for folders and database and etc
app.config['UPLOAD_FOLDER']         = app.config['VAL3DITY_SERVER'] + 'uploads/'
app.config['REPORTS_FOLDER']        = app.config['VAL3DITY_SERVER'] + 'reports/'
app.config['PROBLEMFILES_FOLDER']   = app.config['VAL3DITY_SERVER'] + 'problemfiles/'
app.config['DATABASE']              = app.config['VAL3DITY_SERVER'] + 'val3dity.sqlite'
app.config['ADDGMLIDSEXE']          = 'python %sressources/python/addgmlids.py' % (app.config['VAL3DITY_SERVER'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from .views import *