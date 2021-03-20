python manage.py migrate --noinput
python manage.py collectstatic --noinput
nohup python manage.py process_tasks &