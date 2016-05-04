import os
from xplan import upload_user_csv
from io import BytesIO
import logging
from nose.tools import assert_equal
import time

TEST_CSV = b"""user_id,password,access_level,billing_group\njoe.bloggs%d,password,Adviser,__default__\n""" % time.time()

def spammy_logging():
    try:
        import httplib
    except ImportError:
        import http.client as httplib

    httplib.HTTPConnection.debuglevel = 1

    logging.getLogger().setLevel(logging.DEBUG)

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


class TestUploadUserCsv(object):
    def setup(self):
        self.xplan_username = os.environ["XPLAN_USERNAME"]
        self.xplan_password = os.environ.get("XPLAN_PASSWORD", "")
        self.xplan_url = os.environ["XPLAN_URL"]

    def test_simple_upload(self):
        result = upload_user_csv(self.xplan_url, self.xplan_username,
            self.xplan_password, BytesIO(TEST_CSV))

        assert_equal(len(result), 1)
        assert_equal(result[0]["code"], 201)


spammy_logging()
