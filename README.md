# flask-celery-project

```
sudo apt-get install redis-server
sudo systemctl enable redis-server.service
pip install celery redis
```

```
python app.py
celery -A tasks worker --concurrency=3 --loglevel=DEBUG
```
