from django.views import View
from iasf.apply.models import Application
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime
    
class ApplicationNew(LoginRequiredMixin, View):
    """
    Creates a new application for the user. This is a one-time process.
    """
    def get(self, request, *args, **kwargs):
        if Application.objects.filter(account=self.request.user).exists():
            # don't create multiple forms.
            return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        application = Application(
            account=self.request.user,
            email=self.request.user.email,
            date_created=datetime.now(),
            date_last_modified=datetime.now(),
            finaid_applying_for=int(self.kwargs['finaid_applying_for'])==1
        )
        application.save()
        return HttpResponseRedirect(reverse_lazy('apply:form-page-start'))
        # return super().get(request, *args, **kwargs)
    