from flask import Flask
import os

app = Flask(__name__, static_url_path='')

from .views import *
