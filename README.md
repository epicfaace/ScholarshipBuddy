# DjangoAzure [![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://azuredeploy.net/)

Django makes it easier to build better Web apps more quickly and with less code.[Get started with Django](https://www.djangoproject.com/start/)

env\scripts\pip install -U pip

\env\Scripts\python manage.py migrate

python manage.py colectstatic

```
from django.contrib.auth.models import User
user = User.objects.get(username="epicfaace")
user.is_staff = True
user.is_admin = True
user.save()
```