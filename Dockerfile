# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.6

# install requirements
ADD requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# COPY startup script into known file location in container
COPY start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 80

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    gunicorn iasf.wsgi --log-file - --log-level debug --bind 0.0.0.0:80 --timeout 120

# done!