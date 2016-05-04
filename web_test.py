import os
import requests
import urlparse
from nose.tools import assert_equal, assert_true
from test_util import spammy_logging, TEST_CSV
from io import BytesIO

class TestWeb(object):
    def setup(self):
        self.web_url = os.environ["web_url"]
        self.xplan_url = os.environ["xplan_url"]
        self.xplan_username = os.environ["xplan_username"]
        self.xplan_password = os.environ["xplan_password"]

    def test_upload(self):
        # upload a file and get a task id
        files = [
            ("file", ("file.csv", BytesIO(TEST_CSV), 'text/csv'))
        ]
        response = requests.post(urlparse.urljoin(self.web_url, "/upload_user_csv"),
            data={
                "xplan_url": self.xplan_url,
                "xplan_username": self.xplan_username,
                "xplan_password": self.xplan_password
            },
            files=files)
        assert_equal(response.status_code, 200)

        # ask for the status of the task
        task_id = response.content

        # poll for 10 seconds then give up
        for _ in xrange(10):
            response = requests.get(urlparse.urljoin(self.web_url, "/task/%s" % task_id))
            if response.status_code == 200:
                break
            else:
                assert_equal(response.status_code, 102)
        else:
            assert_true(False)

        task_desc = response.json()
        assert_equal(len(task_desc), 1)
        assert_equal(task_desc[0]["code"], 201)

spammy_logging()