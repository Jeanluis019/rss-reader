release: bash ./deploy_tasks.sh

web: gunicorn --timeout 120 config.wsgi:application --log-file -