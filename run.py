#!/usr/bin/env python

import sys
sys.path.append("src/ct")

from flask import Flask
from rest import api

DEBUG = True
ASSETS_DEBUG = True

SECRET_KEY = "development key"
CT_URL = "https://currenttime.bouvet.no"

app = Flask(__name__)
app.config.from_object(__name__)

app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run("0.0.0.0")