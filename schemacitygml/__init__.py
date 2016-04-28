from flask import Flask

app = Flask(__name__, static_url_path='')

# app.debug = True

class default_settings(object):
    ROOT = '/Users/hugo/www/geovalidation.server/schemacitygml/'

app.config.from_object(default_settings)
app.config.from_envvar('GEOVALIDATION_SETTINGS', silent=True)

#-- fixed setup for folders and database and etc
app.config['UPLOAD_FOLDER'] = app.config['ROOT'] + 'uploads/'

#-- max 50MB file upload
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

from .views import *