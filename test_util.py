import logging
import time

TEST_CSV = b"""user_id,password,access_level,billing_group\njoe.bloggs%d,password,Adviser,__default__\n""" % time.time()

def spammy_logging():
    try:
        import httplib
    except ImportError:
        import http.client as httplib

    httplib.HTTPConnection.debuglevel = 1

    logging.getLogger().setLevel(logging.DEBUG)

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
