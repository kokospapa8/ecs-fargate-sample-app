# Migrate created migrations to database
python manage.py migrate
python manage.py collectstatic

# Start gunicorn server at port 8000 and keep an eye for app code changes
# If changes occur, kill worker and start a new one
gunicorn --reload ecs-sample.wsgi:application -b 0.0.0.0:8000