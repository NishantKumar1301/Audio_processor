#!/usr/bin/env bash
set -o errexit  

pip install -r requirements.txt

python manage.py migrate --fake django_celery_beat zero
python manage.py makemigrations django_celery_beat
python manage.py migrate
