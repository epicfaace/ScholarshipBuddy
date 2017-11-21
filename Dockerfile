# Dockerfile

# FROM directive instructing base image to build upon
FROM python:2.7

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# COPY startup script into known file location in container
COPY start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 80

# CMD specifies the command to execute to start the server running.
#CMD ["python", "manage.py", "runserver"]

#RUN ["python","manage.py","collectstatic","--noinput"]
#RUN ["python","manage.py","migrate", "--noinput"]
#CMD ["gunicorn", "iasf.wsgi", "--log-file", "-", "--log-level", "debug",  "--bind",  "0.0.0.0:80", "--timeout", "120"]

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    gunicorn iasf.wsgi --log-file - --log-level debug --bind 0.0.0.0:80 --timeout 120

# done!