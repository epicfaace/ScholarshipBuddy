from django.views.generic.list import ListView
from django.utils import timezone
from iasf.apply.models import Application
from iasf.review.mixins import UserIsStaffMixin
    
class ReviewList(UserIsStaffMixin, ListView):
    model = Application
    template_name = 'review/reviewList.html'
    login_url = 'login'

    def get_queryset(self):
        return Application.objects.all()
    
    #def get_context_data(self, **kwargs):
    #    context = super(ApplicationList, self).get_context_data(**kwargs)
    #    context['now'] = timezone.now()
    #    return context