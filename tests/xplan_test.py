import csv
from io import BytesIO
import json
import os
from nose.tools import assert_equal, assert_true
import requests
import time
import urlparse

from xit.access_levels import (
    upload_access_level_csv, ACCESS_LEVELS_URL, dump_access_levels_csv)
from xit.users import upload_user_csv

from .test_util import spammy_logging, TEST_USERS_CSV, TEST_ACCESS_LEVELS_CSV


class _Base(object):
    def setup(self):
        self.xplan_username = os.environ["XPLAN_USERNAME"]
        self.xplan_password = os.environ.get("XPLAN_PASSWORD", "")
        self.xplan_url = os.environ["XPLAN_URL"]


class TestUploadUserCsv(_Base):
    def test_simple_upload(self):
        result = upload_user_csv(self.xplan_url, self.xplan_username,
                self.xplan_password, BytesIO(TEST_USERS_CSV % time.time()))

        assert_equal(len(result), 1)
        assert_equal(result[0]["code"], 201)


class TestUploadAccessLevels(_Base):
    def test_simple_upload(self):
        # upload the dummy csv
        result = upload_access_level_csv(self.xplan_url, self.xplan_username,
            self.xplan_password, BytesIO(TEST_ACCESS_LEVELS_CSV % time.time()))

        # check if our webserver claims it worked
        assert_equal(len(result), 2)
        assert_equal(result[0]["code"], 201) # created
        assert_equal(result[1]["code"], 200) # updated

        # check if the data is reflected by XPLAN
        xplan_item_url = urlparse.urljoin(self.xplan_url, ACCESS_LEVELS_URL[1:])
        xplan_item_url += ("/" + json.loads(result[0]["body"])["id"])
        created_access_level = requests.get(xplan_item_url,
                auth=(self.xplan_username, self.xplan_password)).json()

        caps = set(created_access_level["caps"])
        assert_true(created_access_level["name"].startswith("Test Access Level"))
        assert_equal(caps, { "edit_entity_note", "list_group", "login" })


class TestDumpAccessLevels(_Base):
    def test_dump(self):
        result = dump_access_levels_csv(self.xplan_url, self.xplan_username,
            self.xplan_password)
        reader = csv.reader(BytesIO(result))
        next(reader)
        col_header = next(reader)
        assert_true(len(col_header) > 2)
        assert_equal(col_header[:2], ["access_level_id", "access_level_name"])


spammy_logging()
