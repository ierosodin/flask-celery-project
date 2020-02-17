from flask import Flask
from worker import celery


def create_app():
    flask_app = Flask(__name__)
    return flask_app


app = create_app()
app.config['SERVER_NAME'] = '10.20.10.201:5002'


@app.route('/', methods=['GET'])
def index():
    r = celery.send_task('tasks.add', kwargs={'a': 1, 'b': 2})
    return f'{r.id} is waiting for result'

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return f'status: {task.state}<br>result: {task.info}<br>done data: {task.date_done}'
    else:
        return f'status: {task.state}<br>info: {task.info}'


if __name__ == '__main__':
    app.run()
