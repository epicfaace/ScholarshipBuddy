# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from iasf.apply.models import Application
from iasf.apply.forms import ApplicationForm
from iasf.apply.mixins import AjaxableResponseMixin
from django.views.generic.edit import UpdateView
from iasf.apply.schemas import JSONListFieldSchemas
import json

class FormPage(AjaxableResponseMixin, UpdateView):
    template_name = 'apply/formPage.html'
    model = Application
    JSONListFieldSchemas = json.dumps(JSONListFieldSchemas.schema)
    # success_url = reverse_lazy('apply:form-page', step=self.kwargs['step'])
    # form_class = ApplicationForm

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        # todo: error handling here.
        self.success_url = self.request.get_full_path()
        try:
            class ApplicationFormCustom(ApplicationForm):
                class Meta(ApplicationForm.Meta):
                    fieldsets = Application.getFields(int(self.kwargs['step']))
            self.form_class = ApplicationFormCustom
        except ValueError as verr:
            return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        except Exception as ex:
            return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        try:
            self.application = Application.objects.get(account=self.request.user)
        except Application.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        return super(FormPage, self).dispatch(*args, **kwargs)
    def get_object(self):
        return self.application
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(FormPage, self).form_valid(form)

    def get_pages(self):
        """Used by the template to get the page information (for display in the sidebar).
        """
        return Application.pages
    def get_page_number(self):
        """Returns current page number, used by the template.
        """
        return int(self.kwargs['step'])
    def get_should_submit_ajax(self):
        """Should it submit through ajax? This is always true
        except in the case of the page with file uploads, in which it is false.
        """
        return Application.getShouldSubmitAjax(int(self.kwargs['step']))
    def get_is_submit_page(self):
        """Is this submit page? Only true for the last one.
        """
        return Application.getIsSubmitPage(int(self.kwargs['step']))