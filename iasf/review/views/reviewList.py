from django.views.generic.list import ListView
from django.utils import timezone
from iasf.apply.models import Application
from iasf.review.mixins import UserIsStaffMixin
    
class ReviewList(UserIsStaffMixin, ListView):
    model = Application
    template_name = 'review/reviewList.html'
    login_url = 'login'

    def get_queryset(self):
        if not 'filter' in self.kwargs: self.kwargs['filter'] = 'all'
        if self.kwargs['filter'] == 'merit':
            return Application.objects.filter(finaid_applying_for=False)
        elif self.kwargs['filter'] == 'financial':
            return Application.objects.filter(finaid_applying_for=True)
        else:
            return Application.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ReviewList, self).get_context_data(**kwargs)
        context['filter'] = self.kwargs['filter']
        return context