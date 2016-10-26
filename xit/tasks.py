from celery import Celery
from users import upload_user_csv
from access_levels import upload_access_level_csv
import os
import logging
from io import BytesIO

xit_env = os.environ.get("XIT_ENV", "dev")

if xit_env == "dev":
    import celeryconfig_dev as celeryconfig
else:
    import celeryconfig_prod as celeryconfig

app = Celery('tasks', broker=celeryconfig.BROKER_URL)
app.config_from_object(celeryconfig)

logging.info(celeryconfig.BROKER_URL)

@app.task(bind=True)
def process_user_csv(self, xplan_url, xplan_username, xplan_password, csv):
    return upload_user_csv(xplan_url, xplan_username, xplan_password, BytesIO(csv))


@app.task(bind=True)
def process_access_levels_csv(self, xplan_url, xplan_username, xplan_password, csv):
    return upload_access_level_csv(xplan_url, xplan_username, xplan_password, BytesIO(csv))
