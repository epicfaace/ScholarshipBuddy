#!/bin/bash

# Prepare log files and start outputting logs to stdout
touch ./logs/gunicorn.log
touch ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=iasf.settings

exec gunicorn iasf.wsgi:application \
    --name iasf \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --log-file=./logs/gunicorn.log \
    --access-logfile=./logs/gunicorn-access.log \
"$@"