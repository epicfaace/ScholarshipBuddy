from django.conf.urls import url, include
from .views import ForgotUsernameView, ForgotUsernameSuccessView
from .forms import SignupForm
from registration.backends.hmac.views import RegistrationView

urlpatterns = [
    url(r'^registration/register/$', RegistrationView.as_view(form_class=SignupForm), name='registration_register'),
    url(r'^registration/forgot_username/$', ForgotUsernameView.as_view(), name='forgot_username'),
    url(r'^registration/forgot_username_success/$', ForgotUsernameSuccessView.as_view(), name='forgot_username_success'),
    url(r'^registration/', include('registration.backends.hmac.urls')),
    url('^auth/', include('django.contrib.auth.urls'))
]