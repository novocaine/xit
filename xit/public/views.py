# -*- coding: utf-8 -*-
"""
text/html emitting handlers for rendering pages
"""

from flask import render_template

from .forms import CsvUploadForm
from flask import Blueprint

blueprint = Blueprint('views', __name__, static_folder="../static")

@blueprint.route("/")
def home():
    form = CsvUploadForm()
    template_vars = dict(form=form)
    return render_template("public/home.html", **template_vars)