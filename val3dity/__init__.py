from flask import Flask
from celery import Celery

from settings import *

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER']         = UPLOAD_FOLDER
app.config['REPORTS_FOLDER']        = REPORTS_FOLDER
app.config['PROBLEMFILES_FOLDER']   = PROBLEMFILES_FOLDER
app.config['TMP_FOLDER']            = TMP_FOLDER
app.config['DATABASE']              = DATABASE
app.config['CELERY_BROKER_URL']     = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from .views import *