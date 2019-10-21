#!/usr/local/bin/python
# -*- coding: utf-8 -*- 
from flask import jsonify


def json_response(code, msg, data=None):
    return jsonify(code=code, msg=msg, data=data)
