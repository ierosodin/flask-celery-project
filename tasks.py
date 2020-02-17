from celery import Celery
from app import create_app


REDIS = 'redis://127.0.0.1:6379/0'


def make_celery(app):
    app.config['CELERY_ACCEPT_CONTENT'] = ['json']
    app.config['CELERY_TASK_SERIALIZER'] = 'json'
    app.config['CELERY_RESULT_SERIALIZER'] = 'json'
    app.config['CELERY_RESULT_BACKEND'] = REDIS
    app.config['CELERY_BROKER_URL'] = REDIS
    app.config['CELERY_TIMEZONE'] = 'Asia/Taipei'

    _celery = Celery(
        app.import_name,
        backend=REDIS,
        broker=REDIS,
    )
    _celery.conf.update(app.config)

    class ContextTask(_celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    _celery.Task = ContextTask
    return _celery


celery = make_celery(create_app())


@celery.task(bind=True)
def add(self, a, b):
    self.update_state(state='PROGRESS',
                      meta={'current': 10, 'total': 100,
                            'status': 'test'})
    import time
    time.sleep(10)
    return a + b

@celery.task
def error_handler():
    pass
