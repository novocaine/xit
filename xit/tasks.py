from celery import Celery
import time
from users import upload_user_csv
from access_levels import upload_access_level_csv
from io import BytesIO

app = Celery('tasks')

@app.task(bind=True)
def add(self, x, y):
    accum_result = []
    for i in xrange(1000):
        accum_result.append(i)
        time.sleep(1)
        self.update_state(state='PROGRESS',
                meta={'current': i, 'total': accum_result})
    return x + y

@app.task(bind=True)
def process_user_csv(self, xplan_url, xplan_username, xplan_password, csv_filename):
    with open(csv_filename, 'rb') as csv_fileobj:
        return upload_user_csv(xplan_url, xplan_username, xplan_password, csv_fileobj)


@app.task(bind=True)
def process_access_levels_csv(self, xplan_url, xplan_username, xplan_password, csv_filename):
    with open(csv_filename, 'rb') as csv_fileobj:
        return upload_access_level_csv(xplan_url, xplan_username, xplan_password, csv_fileobj)
