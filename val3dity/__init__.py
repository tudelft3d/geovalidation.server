from flask import Flask

from settings import *

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER']       = UPLOAD_FOLDER
app.config['REPORTS_FOLDER']      = REPORTS_FOLDER
app.config['PROBLEMFILES_FOLDER'] = PROBLEMFILES_FOLDER
app.config['TMP_FOLDER']          = TMP_FOLDER
app.config['DATABASE']            = DATABASE



from .views import *