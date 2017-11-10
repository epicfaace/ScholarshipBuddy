# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
#from .widgets import DictionaryWidget, DictionaryArrayWidget
from .fields import JSONListSchemaField

class Application(models.Model):
    """
Documents to upload:
Resume (optional)
SAT / ACT score report (required). -- maybe check with Collegeboard if it can be sent officially and directly to us?
High school transcript -- sent through Parchment?

Additional documents for financial aid:
Financial aid package / cost of attendance letter from the university
Tuition bill for applicant / other dependents if necessary
2016 tax return; 1040 along with supporting documentation
CSS profile report
Any additional documents (optional)

    """
    # todo: make the pages editable (another object?)
    pages = [
        {
            "name": "Personal Information",
            "fields": (
                ("Personal information", {"fields":
                    ("first_name", "middle_name", "last_name", "email", "phone_home", "phone_mobile", "claim_indian_descent")
                }),
                ("Address", {"fields":
                    ("home_address_1",)
                }),
                ("home_address_2",),
                ("home_city", "home_state", "home_zip_code"),
                ("Parent information", {"fields":
                    ("parent_first_name", "parent_middle_name", "parent_last_name")
                })
            )
        },
        {
            "name": "School Information",
            "fields": (
                ("High School", {"fields": (
                    "hs_name", "hs_address_1", "hs_address_2", "hs_city", "hs_state", "hs_zip_code",
                    "hs_counselor_first_name", "hs_counselor_middle_name", "hs_counselor_last_name",
                    "hs_counselor_email")
                }),
                ("Grades and test scores", {"fields": (
                    "hs_gpa", "hs_class_rank","hs_class_size",
                    "scores_sat_reading","scores_sat_math","scores_sat_writing","scores_sat_total",
                    "scores_act_reading","scores_act_math","scores_act_science","scores_act_writing","scores_act_composite",
                    "scores_ap")
                }),
                ("College information", {"fields": (
                    "college_name","college_received_acceptance_letter")
                })
            )
        },
        {
            "name": "Essay",
            "fields": (
                ("essay",)
            )
        },
        {
            "name": "Activities",
            "fields": (
                ("activities",)
            )
        },
        {
            "name": "Upload Files",
            "submitAjax": True,
            "fields": (
                ("file_resume",)
            )
        },
        {
            "name": "Financial Information",
            "fields": (
                ("")
            )
        },
        {
            "name": "Submit",
            "fields": (
                ("")
            )
        }
    ]
    CLAIM_INDIAN_DESCENT_CHOICES = (
        (1, _("Maternal grandparents")),
        (2, _("Paternal grandparents"))
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #todo: blank=False

    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone_home = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name="Home Phone") # validators should be a list
    phone_mobile = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name="Mobile Phone") # validators should be a list
    claim_indian_descent = models.IntegerField(null=True, blank=True, choices=CLAIM_INDIAN_DESCENT_CHOICES, verbose_name="Claim to Indian descent")
    
    home_address_1 = models.CharField(_("address"), max_length=128, blank=True)
    home_address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)
    home_city = models.CharField(_("city"), max_length=64, default="", blank=True)
    home_state = models.CharField(_("state"), max_length=2, default="GA", blank=True)
    home_zip_code = models.CharField(_("Zip Code"), max_length=5, default="", blank=True)

    parent_first_name = models.CharField(max_length=50, blank=True)
    parent_middle_name = models.CharField(max_length=50, blank=True)
    parent_last_name = models.CharField(max_length=50, blank=True)

    # second page:
    hs_name = models.CharField(max_length=100, blank=True)
    
    hs_address_1 = models.CharField(_("Address Line 1"), max_length=128, blank=True)
    hs_address_2 = models.CharField(_("Address Line 2"), max_length=128, blank=True)
    hs_city = models.CharField(_("City"), max_length=64, default="", blank=True)
    hs_state = models.CharField(_("State"), max_length=2, default="GA", blank=True)
    hs_zip_code = models.CharField(_("Zip Code"), max_length=5, default="", blank=True)
    
    hs_counselor_first_name = models.CharField(max_length=50, blank=True)
    hs_counselor_middle_name = models.CharField(max_length=50, blank=True)
    hs_counselor_last_name = models.CharField(max_length=50, blank=True)
    hs_counselor_email = models.EmailField(blank=True)

    hs_gpa = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places = 1)
    hs_class_rank = models.IntegerField(null=True, blank=True)
    hs_class_size = models.IntegerField(null=True, blank=True)

    scores_sat_reading = models.IntegerField(blank=True, null=True)
    scores_sat_math = models.IntegerField(blank=True, null=True)
    scores_sat_writing = models.IntegerField(blank=True, null=True)
    scores_sat_total = models.IntegerField(blank=True, null=True)
    # todo: max min values. 

    scores_act_reading = models.IntegerField(blank=True, null=True)
    scores_act_math = models.IntegerField(blank=True, null=True)
    scores_act_science = models.IntegerField(blank=True, null=True)
    scores_act_writing = models.IntegerField(blank=True, null=True)
    scores_act_composite = models.IntegerField(blank=True, null=True)

    # todo: fix ap exam scores. also do we really want this...?
    scores_ap = JSONListSchemaField(_("AP Exams Taken"), blank=True, null=True)

    college_name = models.CharField(_("College name"), blank=True, max_length=100)
    college_received_acceptance_letter = models.NullBooleanField(_("I have received an acceptance letter."), max_length=100)

    # PAGE 3: ESSAY
    essay = models.TextField(blank=True, null=True)
    
    # PAGE 4: ACTIVITIES
    activities = JSONListSchemaField(name='activities', blank=True, null=True)

    # PAGE 5: UPLOAD FILES:
    file_resume = models.FileField(blank=True, null=True)
    file_sat_scores = models.FileField(blank=True, null=True)
    file_act_scores = models.FileField(blank=True, null=True)
    

    # PAGE 6: FINANCIAL INFORMATION
    income_parent = models.IntegerField(blank=True, null=True)
    income_student = models.IntegerField(blank=True, null=True)
    list_dependents = JSONField(_("List of dependents currently entering college"), blank=True, null=True) # todo: jsonfield.
    college_costs_applicant = models.IntegerField(_("Approximate college cost for applicant"), blank=True, null=True)
    college_costs_dependents = models.IntegerField(_("Approximate college cost for other dependents"), blank=True, null=True)
    income_student = models.IntegerField(_("Expected financial contribution"), blank=True, null=True) # per year? todo

    # financial assistance from other sources
    scholarships_hope = JSONField(blank=True, null=True)
    scholarships_pell = JSONField(blank=True, null=True)
    scholarships_other = JSONField(blank=True, null=True)

    financial_needs_statement = models.TextField(_("Please describe any unusual financial circumstances in your family not listed previously on your application. You may include any information that will be beneficial to the Indian American Scholarship committee. Attach separately, if needed."), blank=True, null=True)

    # form meta fields.
    date_created = models.DateField(null=True, blank=True)
    date_last_submitted = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=False, blank=False, default="2018")

    def __str__(self):
        return self.first_name
    @classmethod
    def getFields(self, number):
        return self.pages[number]["fields"];
    @classmethod
    def getShouldSubmitAjax(self, number):
        if ("submitAjax" in self.pages[number]):
            return self.pages[number]["submitAjax"]
        return False