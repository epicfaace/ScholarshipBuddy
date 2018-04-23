from django.conf.urls import url
from .views import ReviewList, ReviewView, SendEmail
from django.views.generic.base import TemplateView

app_name = 'review'
urlpatterns = [
    url(r'^view/(?P<id>\d+)', ReviewView.as_view(), name='review-view'),
    url(r'^list/(?P<filter_type>.+)/(?P<filter_submitted>.+)', ReviewList.as_view(), name='review-list'),
    url(r'^list/(?P<filter_type>.+)/', ReviewList.as_view(), name='review-list'),
    url(r'^send-email-success/', TemplateView.as_view(template_name="review/mailSuccess.html"), name='send-email-success'),
    url(r'^send-email/', SendEmail.as_view(), name='send-email'),
    url(r'^', ReviewList.as_view(), name='review-list')
]