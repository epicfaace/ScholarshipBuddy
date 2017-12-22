from django.views import View
from iasf.apply.models import Application
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime
    
class ApplicationChangeType(LoginRequiredMixin, View):
    """
    Creates a new application for the user. This is a one-time process.
    """
    def get(self, request, *args, **kwargs):
        application = Application.objects.get(account=request.user)
        application.finaid_applying_for=int(self.kwargs['finaid_applying_for'])==1
        application.save()
        return HttpResponseRedirect(reverse_lazy('apply:application-list'))
        # return super().get(request, *args, **kwargs)