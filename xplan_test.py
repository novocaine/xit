import os
from xplan import upload_user_csv
from io import BytesIO
from nose.tools import assert_equal
from test_util import spammy_logging, TEST_CSV

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
