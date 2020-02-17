from celery import Celery
import os


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND,
                accept_content=['json'],
                task_serializer='json',
                result_serializer='json',
                timezone='Asia/Taipei')


@celery.task(bind=True)
def add(self, a, b):
    self.update_state(state='PROGRESS',
                      meta={'current': 10, 'total': 100,
                            'status': 'test'})
    import time
    time.sleep(10)
    return a + b

