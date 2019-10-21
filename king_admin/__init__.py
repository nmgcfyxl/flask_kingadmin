#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os

from flask import Blueprint

template_folder = os.path.join(os.path.dirname(__file__), "template")

admin = Blueprint("king_admin", __name__, template_folder=template_folder)
