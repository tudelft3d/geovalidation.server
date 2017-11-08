from flask import Flask
from celery import Celery

# from settings import *

app = Flask(__name__, static_url_path='')

app.debug = True

class default_settings(object):
    VAL3DITY_SERVER       = '/Users/hugo/www/geovalidation.server/val3dity/'
    VAL3DITYEXE_FOLDER    = '/Users/hugo/projects/val3dity/build/'
    CELERY_BROKER_URL      = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND  = 'redis://localhost:6379/0'

app.config.from_object(default_settings)
app.config.from_envvar('GEOVALIDATION_SETTINGS', silent=True)

#-- fixed setup for folders and database and etc
app.config['UPLOAD_FOLDER']         = app.config['VAL3DITY_SERVER'] + 'uploads/'
app.config['REPORTS_FOLDER']        = app.config['VAL3DITY_SERVER'] + 'reports/'
app.config['TMP_FOLDER']            = app.config['VAL3DITY_SERVER'] + 'tmp/'
app.config['DATABASE']              = app.config['VAL3DITY_SERVER'] + 'val3dity.sqlite'

#-- max 50MB file upload
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from .views import *