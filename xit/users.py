"""
Upload users via CSV
"""

import csv
import itertools
import random

from xit import xplan

PARAM_COLUMNS = ("access_level", "billing_group", "user_id", "password")

def _validate_fields(fields):
    for p in PARAM_COLUMNS:
        if p not in fields:
            raise ValueError("missing %s column; %s" % (p, fields))


def _user_fields_to_batch_data(url, rows_of_fields):
    payload = []
    for fields in rows_of_fields:
        _validate_fields(fields)

        if 'user_id' in fields:
            fields['user_id'] = fields['user_id'].replace('RAND', str(random.randint(1, 100000000)))

        body = {
            "fields": { k: v for k, v in fields.iteritems()
                if k not in PARAM_COLUMNS },
        }

        body.update({ p: fields[p] for p in PARAM_COLUMNS })

        payload.append({
            "method": "POST",
            "url": url,
            "body": body
        })

    return {
        "batch": payload
    }


def upload_user_csv(xplan_url, xplan_username, xplan_password, csvfile):
    return xplan.upload_csv(xplan_url, "/resourceful/entity/user-v2", xplan_username, xplan_password, csvfile, 10,
            _user_fields_to_batch_data)
