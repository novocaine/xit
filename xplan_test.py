import os
from xplan import upload_user_csv
from io import BytesIO

TEST_CSV = b"""userid\njoe.bloggs\n"""

class TestUploadUserCsv(object):
    def setup(self):
        self.xplan_username = os.environ["XPLAN_USERNAME"]
        self.xplan_password = os.environ["XPLAN_PASSWORD"]
        self.xplan_url = os.environ["XPLAN_URL"]

    def test_auth(self):
        upload_user_csv(self.xplan_url, self.xplan_username,
                self.xplan_password, BytesIO(TEST_CSV))
