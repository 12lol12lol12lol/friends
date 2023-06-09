#!/bin/bash
ptyhon manage.py collectstatic
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 \
         --reload \
         --timeout 600 \
         src.wsgi:application
