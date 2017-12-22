from django.conf.urls import url
from .views import FormPage, ApplicationList, ApplicationNew

app_name = 'apply'
urlpatterns = [
    url(r'^new/(?P<finaid_applying_for>\d+)/', ApplicationNew.as_view(), name='application-new'),
    url(r'^form/$', FormPage.as_view(), name='form-page-start', kwargs={'step':0}),
    url(r'^form/(?P<step>\d+)/$', FormPage.as_view(), name='form-page'),
    url(r'^$', ApplicationList.as_view(), name='application-list')
]