from celery import Celery
import time

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
