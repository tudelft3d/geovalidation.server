from flask import Flask
# from settings import *

app = Flask(__name__, static_url_path='')

class default_settings(object):
    PREPAIREXE            = '/Users/hugo/projects/prepair/prepair'
    WKT_MAXSIZE           = 1e4

app.config.from_object(default_settings)
app.config.from_envvar('GEOVALIDATION_SETTINGS', silent=True)

from .views import *