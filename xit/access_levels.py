"""
Upload access levels to XPLAN via CSV
"""

import csv
import itertools
import xplan
import requests
import urlparse
from io import BytesIO


ACCESS_LEVELS_URL = "/resourceful/sysadmin/user/access_level"
CAPS_URL = "/resourceful/sysadmin/capability/user"


def _access_level_fields_to_batch_data(collection_url, rows_of_fields):
    payload = []

    for fields in rows_of_fields:
        caps = [field for field, cell_value in fields.iteritems()
                if cell_value and field not in ("access_level_name", "access_level_id")]

        if fields.get("access_level_id"):
            # overwrite (ignores name)
            body = {
                "caps": caps
            }
            method = "PUT"
            url = collection_url + "/" + fields["access_level_id"]
        elif fields.get("access_level_name"):
            # create
            body = {
                "name": fields["access_level_name"],
                "caps": caps
            }
            method = "POST"
            url = collection_url

        else:
            # skip line? hrm
            continue

        payload.append({
            "method": method,
            "url": url,
            "body": body
        })

    return {
        "batch": payload
    }


def upload_access_level_csv(xplan_url, xplan_username, xplan_password, csvfile):
    return xplan.upload_csv(xplan_url, ACCESS_LEVELS_URL, xplan_username, xplan_password, csvfile, 10,
            _access_level_fields_to_batch_data)


def dump_access_levels_csv(xplan_url, xplan_username, xplan_password):
    if not xplan_url.endswith("/"):
        xplan_url += "/"

    session = requests.Session()
    session.auth = (xplan_username, xplan_password)

    caps = session.get(urlparse.urljoin(xplan_url, CAPS_URL[1:]))
    caps.raise_for_status()
    caps = caps.json()

    access_levels = session.get(urlparse.urljoin(xplan_url, ACCESS_LEVELS_URL[1:]))
    access_levels.raise_for_status()
    access_levels = access_levels.json()

    b = BytesIO()
    writer = csv.writer(b)

    # blurp out the human readable titles for reference. lines beginning with '#' are ignored by our readers
    writer.writerow(["#", ""] + [cap["title"] for cap in caps])
    writer.writerow(["access_level_id", "access_level_name"] + [cap["id"] for cap in caps])

    for level in access_levels:
        level_caps = set(level["caps"])
        writer.writerow([level["id"], level["name"]] +
                ["X" if cap["id"] in level_caps else "" for cap in caps])

    return b.getvalue()
