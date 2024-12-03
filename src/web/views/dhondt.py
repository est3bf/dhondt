#!/usr/bin/python3

from flask import render_template
from flask import Blueprint

dhondt_view = Blueprint("dhondt_view", __name__)


@dhondt_view.route("/")
def home():
    return render_template("dhondt.html")
