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

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app by default.
    """
    return {'app': app}


@manager.command
def test(web_url=None, username=None, password=None, xplan_url=None):
    """Run the tests."""
    import nose
    os.environ["WEB_URL"] = web_url
    os.environ["XPLAN_USERNAME"] = username
    os.environ["XPLAN_PASSWORD"] = password
    os.environ["XPLAN_URL"] = xplan_url
    exit_code = nose.run(argv=[TEST_PATH, 'tests.web_test', '--verbose'])
    exit_code = nose.run(argv=[TEST_PATH, 'tests.xplan_test', '--verbose'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    manager.run()
