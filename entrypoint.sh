#!/bin/bash
#python manage.py makemigrations --noinput
#python manage.py migrate --noinput
# gunicorn config.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
