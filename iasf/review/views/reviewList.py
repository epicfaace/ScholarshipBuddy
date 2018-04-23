from django.views.generic.list import ListView
from django.utils import timezone
from iasf.apply.models import Application
from iasf.review.mixins import UserIsStaffMixin
    
class ReviewList(UserIsStaffMixin, ListView):
    model = Application
    template_name = 'review/reviewList.html'
    login_url = 'login'

    def get_queryset(self):
        query_kwargs = {}
        filter_type = self.kwargs.setdefault('filter_type', 'all')
        filter_submitted = self.kwargs.setdefault('filter_submitted', 'all')
        if filter_type == 'merit':
            query_kwargs["finaid_applying_for"] = False
        elif filter_type == 'financial':
            query_kwargs["finaid_applying_for"] = True
        if filter_submitted == 'submitted':
            query_kwargs["submitted"] = True
        elif filter_submitted == 'progress':
            query_kwargs["submitted"] = False
        return Application.objects.filter(**query_kwargs)
        
        # else:
        #     return Application.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ReviewList, self).get_context_data(**kwargs)
        context['filter_type'] = self.kwargs['filter_type']
        context['filter_submitted'] = self.kwargs['filter_submitted']
        return context