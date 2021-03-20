release: bash ./deploy_tasks.sh
worker: python manage.py process_tasks
web: gunicorn --timeout 120 config.wsgi:application --log-file -