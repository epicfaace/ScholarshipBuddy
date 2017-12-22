from django.conf.urls import url, include
from .views import SignupView
from .forms import SignupForm
from registration.backends.hmac.views import RegistrationView

urlpatterns = [
    url(r'^registration/register/$', RegistrationView.as_view(form_class=SignupForm), name='registration_register'),
    url(r'^registration/', include('registration.backends.hmac.urls')),
    url('^auth/', include('django.contrib.auth.urls')),
    #url('^signup', SignupView.as_view(), name='signup' )
]