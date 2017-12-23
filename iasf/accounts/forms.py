from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

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
    def clean_email(self):
        """
        Don't allow for duplicate emails.
        """
        email = self.cleaned_data['email']
        unique_email = True
        #existingUsernames = []
        for user in User.objects.filter(email=email):
            unique_email = False
        if (unique_email):
            return email
        else:
            raise forms.ValidationError(
                mark_safe("An account with that email address already exists. Click on <a href=\"{0}\">\"Forgot username\"</a> to have your username emailed to you.").format(reverse_lazy('forgot_username'))
            )
        return email
        #    existingUsernames.append()

class ForgotUsernameForm(forms.Form):
    email = forms.EmailField()

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