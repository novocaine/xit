from __future__ import print_function
import requests
import csv
import urlparse
import itertools
import json


def _grouper(iterable, n):
    # modified itertools recipe for chunking inputs
    args = [iter(iterable)] * n
    return (filter(None, x) for x in itertools.izip_longest(*args))


def _get_users_from_csv(csvfile):
    # yield dicts of entity fields
    reader = csv.reader(csvfile)
    colheaders = next(reader)

    # TODO: validate colheaders?

    for row in reader:
        fields = {
            colheader: field
            for colheader, field in itertools.izip(colheaders, row)
        }

        yield fields


def _fields_to_batch_data(url, rows_of_fields):
    return {
        "batch": [
            {
                "method": "POST",
                "url": url,
                "body": {
                    "fields": fields
                }
            }
            for fields in rows_of_fields
        ]
    }


def upload_user_csv(xplan_url, xplan_username, xplan_password, csvfile):
    resourceful_url = urlparse.urljoin(xplan_url, "resourceful")

    session = requests.Session()
    session.auth = (xplan_username, xplan_password)

    USER_CHUNKSIZE = 10

    users_url = "/resourceful/entity/user"

    result = []

    for fields in _grouper(_get_users_from_csv(csvfile), USER_CHUNKSIZE):
        # TODO - check how this sends auth headers
        response = session.post(resourceful_url,
                                data=json.dumps(_fields_to_batch_data(users_url, fields)),
                                headers={"Content-Type": "application/json"})
        response.raise_for_status()
        result.extend(response.json())

    return result
