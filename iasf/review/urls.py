from django.conf.urls import url
from .views import ReviewList, ReviewView

app_name = 'review'
urlpatterns = [
    url(r'^view/(?P<id>\d+)', ReviewView.as_view(), name='review-view'),
    url(r'^list/(?P<filter>.+)', ReviewList.as_view(), name='review-list'),
    url(r'^', ReviewList.as_view(), name='review-list')
]