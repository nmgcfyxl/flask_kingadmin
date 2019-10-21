#!/usr/local/bin/python
# -*- coding: utf-8 -*- 
from flask import Flask
from flask_babel import Babel

from admin import admin

app = Flask(__name__)

babel = Babel(app)
app.config["DEBUG"] = True
app.config["BABEL_DEFAULT_LOCALE"] = "zh"

app.register_blueprint(admin)

if __name__ == '__main__':
    app.run()
