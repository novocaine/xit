import requests
import csv
import urlparse
import itertools

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


def _fields_to_user_desc(fields):
    # convert dict of colheader -> cell value to what we are 
    # sending the api
    return {
        "fields": fields
    }


def upload_user_csv(xplan_url, xplan_username, xplan_password, csvfile):
    resourceful_url = urlparse.urljoin(xplan_url, "/resourceful")
    
    session = requests.Session()
    session.auth = (xplan_username, xplan_password)

    USER_CHUNKSIZE = 10

    users_url = urlparse.urljoin(resourceful_url, "/entity/user")

    result = []

    for fields in _grouper(_get_users_from_csv(csvfile), USER_CHUNKSIZE):
        # TODO - check how this sends auth headers
        response = requests.post(users_url, data=_fields_to_user_desc(fields), 
                                 headers={"Content-Type": "application/json"})
        result.extend(response.json())

    return result
