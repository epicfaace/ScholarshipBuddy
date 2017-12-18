from iasf.review.mixins import UserIsStaffMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from iasf.apply.models import Application
from iasf.apply.forms import ApplicationForm
from django.views.generic.edit import UpdateView
from iasf.apply.schemas import JSONListFieldSchemas
import json
from django.db.models import AutoField
from django.core.exceptions import ValidationError
from django.contrib import messages


class ReviewView(UserIsStaffMixin, UpdateView):
    template_name = 'review/reviewView.html'
    model = Application 
    JSONListFieldSchemas = json.dumps(JSONListFieldSchemas.schema)
    # success_url = reverse_lazy('apply:form-page', kwargs={'step':self.kwargs['step']})
    # form_class = ApplicationForm

    def dispatch(self, *args, **kwargs):
        """Checks to see if an ApplicationForm is already present for the user;
           if not, redirects them to the appropriate page.
        """
        # todo: error handling here.
        self.success_url = self.request.get_full_path()
        self.form_pages = []
        for step, page in enumerate(Application.pages):
            try:
                # step = int(self.kwargs['step'])
                class ApplicationFormCustom(ApplicationForm):
                    class Meta(ApplicationForm.Meta):
                        fieldsets = Application.getFields(step)
                self.form_class = ApplicationFormCustom
                self.form_pages.append(ApplicationFormCustom)
            except ValueError as verr:
                return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
            except Exception as ex:
                return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        try:
            self.application = Application.objects.get(pk=self.kwargs['id'])
            #self.object = self.application
        except Application.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('apply:application-new'))
        return super(ReviewView, self).dispatch(*args, **kwargs)
    def get_object(self):
        """Behaves the same as form_class attribute -- but this lets one
           subclass ApplicationForm so that only certain fieldsets are displayed from it.
        """
        return self.application
    def get_context_data(self, **kwargs):
        context = super(ReviewView, self).get_context_data(**kwargs)
        context['form_pages'] = self.form_pages
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