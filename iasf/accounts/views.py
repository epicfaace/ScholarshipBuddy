# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SignupForm, ForgotUsernameForm

class ForgotUsernameView(FormView):
    template_name = 'registration/forgot_username.html'
    form_class = ForgotUsernameForm
    success_url = reverse_lazy('forgot_username_success')
    email_subject_template = 'registration/forgot_username_subject.txt'
    email_body_template = 'registration/forgot_username_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = None
        for user in User.objects.filter(email=email):
            user = user
            break
        if not user:
            form.errors[forms.forms.NON_FIELD_ERRORS] = "No account found for the email address you entered."
            return self.form_invalid(form)
        
        context = {
            'username': user.username,
            'protocol': self.request.scheme + 'a',
            'domain': self.request.get_host()
        }
        subject = render_to_string(self.email_subject_template,
                                   context)
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.email_body_template,
                                   context)
        
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        return HttpResponseRedirect(reverse_lazy('forgot_username_success'))

class ForgotUsernameSuccessView(TemplateView):
    template_name = 'registration/forgot_username_success.html'