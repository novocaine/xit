import logging

TEST_USERS_CSV = b"""user_id,password,access_level,billing_group
joe.bloggs%d,password,Adviser,__default__\n"""
TEST_ACCESS_LEVELS_CSV = b"""access_level_name,access_level_id,edit_entity_note,list_group,login,client_focus,allow_email
Test Access Level %s,,X,X,X,,
,5,,,,,,""" # '5' is 'receptionist'

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
