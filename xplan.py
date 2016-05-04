"""
XPLAN API helper functions
"""

import requests
import urlparse
import json
import itertools
import csv


def _grouper(iterable, n):
    # modified itertools recipe for chunking inputs
    args = [iter(iterable)] * n
    return (filter(None, x) for x in itertools.izip_longest(*args))


def _get_fields_from_csv(csvfile):
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


def upload_csv(xplan_url, url, xplan_username, xplan_password, csvfile, chunksize, fields_to_batch_data):
    resourceful_url = urlparse.urljoin(xplan_url, "resourceful")

    session = requests.Session()
    session.auth = (xplan_username, xplan_password)

    USER_CHUNKSIZE = 10

    result = []

    for fields in _grouper(_get_fields_from_csv(csvfile), USER_CHUNKSIZE):
        # TODO - check how this sends auth headers
        response = session.post(resourceful_url,
                                data=json.dumps(fields_to_batch_data(url, fields)),
                                headers={"Content-Type": "application/json"})
        response.raise_for_status()
        result.extend(response.json())

    return result
