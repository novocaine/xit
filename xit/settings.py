# -*- coding: utf-8 -*-
import os
import tempfile


class Config(object):
    SECRET_KEY = os.environ.get(
        'XIT_SECRET',
        'secret-key')
    APP_DIR = os.path.abspath(
        os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    UPLOAD_FOLDER = tempfile.gettempdir() # TODO put them somewhere secure

    SITE_NAME = 'XIT: XPLAN Implementation Toolkit'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False  # Allows form testing
