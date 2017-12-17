# IASF apply website
Website for the Indian American Scholarship Foundation application.
URL: http://apply.iasf.org/

Django makes it easier to build better Web apps more quickly and with less code.[Get started with Django](https://www.djangoproject.com/start/)

env\scripts\pip install -U pip

\env\Scripts\python manage.py migrate --noinput

python manage.py collectstatic 

```
from django.contrib.auth.models import User
user = User.objects.get(username="epicfaace")
user.is_staff = True
user.is_admin = True
user.save()
```

pip install -e git+git://github.com/epicfaace/django-validated-file.git#egg=django-validate
d-file

# Docker
sudo service docker start

# Docker compose with nginx
http://ruddra.com/2016/08/14/docker-django-nginx-postgres/
http://ruddra.com/2016/11/02/serve-static-files-by-nginx-from-django-using-docker/

Did you know that Microsoft gives away $5,000 in Azure credits to nonprofits? Learn how I used Azure to get a nonprofit website up and running for free. #azure #microsoft #django #docker #nonprofits