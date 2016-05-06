from io import BytesIO
import os
import requests
import time
import urlparse

from nose.tools import assert_equal, assert_true

from .test_util import spammy_logging, TEST_USERS_CSV


class TestWeb(object):
    def setup(self):
        self.web_url = os.environ["WEB_URL"]
        self.xplan_url = os.environ["XPLAN_URL"]
        self.xplan_username = os.environ["XPLAN_USERNAME"]
        self.xplan_password = os.environ["XPLAN_PASSWORD"]

    def test_upload(self):
        """
        Tests what looks like success from an HTTP code perspective, but doesn't look
        at any of the data. Intent is to check the celery glue.
        """

        # upload a file and get a task id
        files = [
            ("file", ("file.csv", BytesIO(TEST_USERS_CSV % time.time()), 'text/csv'))
        ]
        response = requests.post(urlparse.urljoin(self.web_url, "/upload_csv/users"),
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
                time.sleep(1)
        else:
            assert_true(False)

        # does it look like it worked??
        task_desc = response.json()
        assert_equal(len(task_desc), 1)
        assert_equal(task_desc[0]["code"], 201)


spammy_logging()
