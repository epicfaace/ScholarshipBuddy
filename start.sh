#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn iasf.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 3