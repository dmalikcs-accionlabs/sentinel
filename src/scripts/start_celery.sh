#
export CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
export  DJANGO_SETTINGS_MODULE="sentinel.settings_local"
celery worker -A sentinel.celery -l debug