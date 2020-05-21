#
export CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
celery worker -A sentinel.celery -l debug