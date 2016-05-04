import os
from users import upload_user_csv
from access_levels import upload_access_level_csv
from io import BytesIO
from nose.tools import assert_equal
from test_util import spammy_logging, TEST_USERS_CSV, TEST_ACCESS_LEVELS_CSV


class _Base(object):
    def setup(self):
        self.xplan_username = os.environ["XPLAN_USERNAME"]
        self.xplan_password = os.environ.get("XPLAN_PASSWORD", "")
        self.xplan_url = os.environ["XPLAN_URL"]


class TestUploadUserCsv(_Base):
    def test_simple_upload(self):
        result = upload_user_csv(self.xplan_url, self.xplan_username,
                self.xplan_password, BytesIO(TEST_USERS_CSV))

        assert_equal(len(result), 1)
        assert_equal(result[0]["code"], 201)

class TestUploadAccessLevels(_Base):
    def test_simple_upload(self):
        result = upload_access_level_csv(self.xplan_url, self.xplan_username,
            self.xplan_password, BytesIO(TEST_ACCESS_LEVELS_CSV))

        assert_equal(len(result), 1)
        assert_equal(result[0]["code"], 201)

spammy_logging()
