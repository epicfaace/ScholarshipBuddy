# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import SignupForm
from django.urls import reverse_lazy

# Create your views here.
class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        instance = form.save()
        # self.cleaned_data['temp_id']
        return super(SignupView, self).form_valid(form)