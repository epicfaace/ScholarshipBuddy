from django.conf.urls import url, include
from .views import SignupView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^signup', SignupView.as_view(), name='signup' )
]