from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

class SignupForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        # Make all fields required on the form:
        for key in self.fields:
            self.fields[key].required = True
            help_text = self.fields[key].help_text
            self.fields[key].help_text = None
            if help_text != '':
                self.fields[key].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body', 'data-html': 'true'})

class SignupFormOld(UserCreationForm):
    """
    Form used to create a new account.
    """
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        # Make all fields required on the form:
        for key in self.fields:
            self.fields[key].required = True
            help_text = self.fields[key].help_text
            self.fields[key].help_text = None
            if help_text != '':
                self.fields[key].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body', 'data-html': 'true'})