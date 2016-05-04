"""
Upload access levels to XPLAN via CSV
"""

import csv
import itertools
import xplan


def _access_level_fields_to_batch_data(url, rows_of_fields):
    payload = []
    for fields in rows_of_fields:
        body = {
            "name": fields["access_level"],
            "caps": [field for field, cell_value in fields.iteritems() if cell_value and field != "access_level"]
        }

        payload.append({
            "method": "POST",
            "url": url,
            "body": body
        })

    return {
        "batch": payload
    }

def upload_access_level_csv(xplan_url, xplan_username, xplan_password, csvfile):
    return xplan.upload_csv(xplan_url, "/resourceful/sysadmin/user/access_level", xplan_username, xplan_password, csvfile, 10,
            _access_level_fields_to_batch_data)
