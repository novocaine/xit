#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls

from xit.app import create_app
from xit.settings import DevConfig, ProdConfig

if os.environ.get("XIT_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)

# This is for Amazon EB which looks for an object called 'application'
# - don't change this
application = app


def _make_context():
    """Return context dict for a shell session so you can access
    app by default.
    """
    return {'app': app}


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    manager.run()
