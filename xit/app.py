# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

from flask import Flask, render_template

from xit.settings import ProdConfig
from xit.extensions import (
    bs,
)
from xit.public.views import blueprint as public_bp


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    bs.init_app(app)

    return None


def register_blueprints(app):
    app.register_blueprint(public_bp)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return (render_template("{0}.html".format(error_code)),
                error_code)
    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
