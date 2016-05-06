from celeryconfig import *

BROKER_TRANSPORT = "sqs"
BROKER_URL = "redis://localhost:6379/0"
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-west-2'
}

BROKER_USER = AWS_ACCESS_KEY_ID
BROKER_PASSWORD = AWS_SECRET_ACCESS_KEY
