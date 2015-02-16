from flask import Flask
from celery import Celery

# from settings import *

app = Flask(__name__, static_url_path='')

class default_settings(object):
    ROOT_FOLDER_VAL3DITY  = '/Users/hugo/www/geovalidation/val3dity/'
    UPLOAD_FOLDER         = ROOT_FOLDER_VAL3DITY + 'uploads/'
    REPORTS_FOLDER        = ROOT_FOLDER_VAL3DITY + 'reports/'
    PROBLEMFILES_FOLDER   = ROOT_FOLDER_VAL3DITY + 'problemfiles/'
    DATABASE              = ROOT_FOLDER_VAL3DITY + 'val3dity.sqlite'
    TMP_FOLDER            = '/tmp/'
    CELERY_BROKER_URL     = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app.config.from_object(default_settings)
app.config.from_envvar('GEOVALIDATION_SETTINGS', silent=True)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from .views import *