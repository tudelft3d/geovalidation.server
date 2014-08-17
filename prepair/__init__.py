from flask import Flask

from settings import *

app = Flask(__name__, static_url_path='')

from .views import *