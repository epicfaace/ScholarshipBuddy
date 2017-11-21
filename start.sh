#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec python manage.py collectstatic --noinput
exec python manage.py migrate --noinput
exec gunicorn iasf.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 3