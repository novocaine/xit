from celeryconfig import *
import os
endpoint = os.environ["REDIS_ENDPOINT_ADDRESS"]

BROKER_URL = "redis://%s:6379/0" % endpoint
CELERY_RESULT_BACKEND = "redis://%s:6379/0" % endpoint