from iasf.review.mixins import UserIsStaffMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from iasf.apply.models import Application
from iasf.apply.forms import ApplicationForm
from django.views.generic.base import TemplateView
from iasf.apply.schemas import JSONListFieldSchemas
import json
from django.db.models import AutoField
from django.core.exceptions import ValidationError
from django.contrib import messages


class ReviewView(UserIsStaffMixin, TemplateView):
    template_name = 'review/reviewView.html'
    JSONListFieldSchemas = json.dumps(JSONListFieldSchemas.schema)
    # success_url = reverse_lazy('apply:form-page', kwargs={'step':self.kwargs['step']})
    # form_class = ApplicationForm

    def dispatch(self, *args, **kwargs):
        # todo: error handling here.
        try:
            self.application = get_object_or_404(Application, pk=self.kwargs['id'])
            #self.object = self.application
        except Application.DoesNotExist:
            return HttpResponseNotFound('<h1>Application not found</h1>')
        self.success_url = self.request.get_full_path()
        self.form_pages = []
        # self.fields['sku'].widget.attrs['readonly'] = True
        for step, page in enumerate(Application.pages):
            if (not self.application.finaid_applying_for and 'financialOnly' in page and page['financialOnly'] == True):
                continue
            class ApplicationFormCustom(ApplicationForm):
                def __init__(self, *args, **kwargs):
                    super(ApplicationFormCustom, self).__init__(*args, **kwargs)
                    for field in self.fields:
                        self.fields[field].widget.attrs['disabled'] = True
                class Meta(ApplicationForm.Meta):
                    fieldsets = Application.getFields(step)
            self.form_class = ApplicationFormCustom
            self.form_pages.append(ApplicationFormCustom(initial=self.application.__dict__))
        return super(ReviewView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ReviewView, self).get_context_data(**kwargs)
        context['form_pages'] = self.form_pages
        context['application'] = self.application
        return context
"""
class ReviewView(UserIsStaffMixin, ListView):
    model = Application
    template_name = 'review/reviewList.html'
    login_url = 'login'

    def get_queryset(self):
        return Application.objects.all()
    
    #def get_context_data(self, **kwargs):
    #    context = super(ApplicationList, self).get_context_data(**kwargs)
    #    context['now'] = timezone.now()
    #    return context
"""