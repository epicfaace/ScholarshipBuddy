from django import forms
from .models import Application
from betterforms.forms import BetterModelForm

class ApplicationForm(BetterModelForm):
    """
    Abstract class for application form page. An instance of this form is created in formPage.py with the
    "fields" attribute overriden to match the fields seen in a specific page.
    """
    redirect = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        abstract = True
        model = Application
        fieldsets =  Application.getFields(0)
        widgets = {
            'a': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'college_received_acceptance_letter': forms.Select(choices=[(None, "Select an option"), (True, "Yes"), (False, "No")]),
            # 'scores_ap': forms.HiddenInput(attrs= {'data-type': 'dictionaryList', 'data-schema': ScoresAPField.getProperties()})
        }
    name = "A"