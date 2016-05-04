from celery import Celery
import time
from xplan import upload_user_csv

app = Celery('tasks')
app.config_from_object("celeryconfig")

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
def process_user_csv(self, csv):
    upload_user_csv() 
