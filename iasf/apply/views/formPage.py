# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from iasf.apply.models import Application, ApplicationInProgress
from iasf.apply.forms import ApplicationForm, ApplicationFormInProgress
from iasf.apply.mixins import AjaxableResponseMixin
from django.views.generic.edit import UpdateView
from iasf.apply.schemas import JSONListFieldSchemas
import json
from django.db.models import AutoField
from django.core.exceptions import ValidationError
from django.contrib import messages

class FormPage(AjaxableResponseMixin, UpdateView):
    template_name = 'apply/formPage.html'
    model = ApplicationInProgress
    JSONListFieldSchemas = json.dumps(JSONListFieldSchemas.schema)
    # success_url = reverse_lazy('apply:form-page', kwargs={'step':self.kwargs['step']})
    # form_class = ApplicationFormInProgress

    def dispatch(self, *args, **kwargs):
        """Checks to see if an ApplicationFormInProgress is already present for the user;
           if not, redirects them to the appropriate page.
        """
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        # todo: error handling here.
        self.success_url = self.request.get_full_path()
        try:
            step = int(self.kwargs['step'])
            class ApplicationFormCustom(ApplicationFormInProgress):
                class Meta(ApplicationForm.Meta):
                    fieldsets = Application.getFields(step)
            self.form_class = ApplicationFormCustom
        except ValueError as verr:
            return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        except Exception as ex:
            return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        try:
            self.application = ApplicationInProgress.objects.get(account=self.request.user)
            #self.object = self.application
        except ApplicationInProgress.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('apply:application-new'))
        return super(FormPage, self).dispatch(*args, **kwargs)
    def get_object(self):
        """Behaves the same as form_class attribute -- but this lets one
           subclass ApplicationFormInProgress so that only certain fieldsets are displayed from it.
        """
        return self.application
        
    def post(self, request, *args, **kwargs):
        """Special handling for final submit page -- save this in the actual form as well!"""
        step = int(self.kwargs['step'])
        object = self.get_object()
        if (Application.getIsSubmitPage(step)):
            # todo: add date submitted to form.
            super(FormPage, self).post(request, *args, **kwargs) # save incomplete form.
            completedApp = self.copy_model_instance(object, Application)
            try:
                completedApp.full_clean()
                completedApp.save()
                return HttpResponseRedirect(reverse_lazy('apply:application-list')) #todo: success
            except ValidationError as e:
                # Do something based on the errors contained in e.message_dict.
                print e
                messages.add_message(request, messages.ERROR, 'Error submitting: ' + str(e.message_dict))
                return HttpResponseRedirect(reverse_lazy('apply:form-page', kwargs={'step':step}))
        else:
            return super(FormPage, self).post(request, *args, **kwargs)

    def copy_model_instance(self, obj, toClass=None):
        """Copies model. Based on https://djangosnippets.org/snippets/1040/
        """
        if toClass is None:
            toClass = obj.__class__
        initial = dict([(f.name, getattr(obj, f.name))
                        for f in obj._meta.fields
                        if not isinstance(f, AutoField) and\
                        not f in obj._meta.parents.values()])
        return toClass(**initial)

    def form_valid(self, form):
        """This method is called when valid form data has been POSTed.
        Redirects to "redirect" input value."""
        if not self.request.is_ajax() and 'redirect' in form.cleaned_data:
            def successUrlFn():
                return form.cleaned_data['redirect']
            self.get_success_url = successUrlFn
        return super(FormPage, self).form_valid(form)
    def form_invalid(self, form):
        """When form is invalid, that's ok; show the error messages, but still save the other valid data.
        """
        #def clean_new(self):
        #    return self.cleaned_data
        #form.instance.clean = clean_new
        #form.save()
        return super(FormPage, self).form_invalid(form)
    
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