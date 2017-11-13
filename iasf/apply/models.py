# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
#from .widgets import DictionaryWidget, DictionaryArrayWidget
from .fields import JSONListSchemaField, DocumentField

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
            "name": "Financial Information",
            "fields": (
                "finaid_applying_for",
                ("Income", {"fields": (
                    "finaid_income_parent", "finaid_income_student",)
                }),
                ("finaid_list_dependents",),
                ("College costs", {"fields": (
                    "finaid_college_costs_applicant", "finaid_college_costs_dependents", "finaid_expected_contribution")
                }),
                ("Scholarships", {"fields": (
                    "finaid_scholarships_hope",
                    "finaid_scholarships_pell",
                    "finaid_scholarships_other",)
                }),
                ("Financial Needs Statement", {"fields": (
                    "finaid_needs_statement",)
                }),
            )
        },
        {
            "name": "Upload Files",
            "submitAjax": True,
            "fields": (
                ("Academic", {"fields": (
                    "file_resume",)
                }),
                ("file_transcript",),
                ("file_sat_scores",),
                ("file_act_scores",),
                ("Financial Aid", {"fields": (
                    "file_finaid_cost",)
                }),
                ("file_finaid_tuition",),
                ("file_finaid_taxreturn",),
                ("file_finaid_cssprofile",),
                ("file_finaid_additional",)
            )
        },
        {
            "name": "Submit",
            "submitPage": True,
            "fields": (
                ("Sign and submit", {"fields": (
                    "signature",)
                }),
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
    
    home_address_1 = models.CharField(_("Address Line 1"), max_length=128, blank=True)
    home_address_2 = models.CharField(_("Address Line 2"), max_length=128, blank=True)
    home_city = models.CharField(_("City"), max_length=64, default="", blank=True)
    home_state = models.CharField(_("State"), max_length=2, default="GA", blank=True)
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

    hs_gpa = models.DecimalField(_("HS GPA (100 or 4.0 scale)"), blank=True, null=True, max_digits=3, decimal_places = 1)
    hs_class_rank = models.IntegerField(null=True, blank=True)
    hs_class_size = models.IntegerField(null=True, blank=True)

    scores_sat_reading = models.IntegerField(_("SAT Score - reading"), blank=True, null=True)
    scores_sat_math = models.IntegerField(_("SAT Score - math"), blank=True, null=True)
    scores_sat_writing = models.IntegerField(_("SAT Score - writing"), blank=True, null=True)
    scores_sat_total = models.IntegerField(_("SAT Score - total"), blank=True, null=True)
    # todo: max min values. 

    scores_act_reading = models.IntegerField(_("ACT Score - reading"), blank=True, null=True)
    scores_act_math = models.IntegerField(_("ACT Score - math"), blank=True, null=True)
    scores_act_science = models.IntegerField(_("ACT Score - science"), blank=True, null=True)
    scores_act_writing = models.IntegerField(_("ACT Score - writing"), blank=True, null=True)
    scores_act_composite = models.IntegerField(_("ACT Score - composite"), blank=True, null=True)

    # todo: Do we really want this...?
    scores_ap = JSONListSchemaField(_("AP Exams Taken"), schema="scores_ap", blank=True, null=True)

    college_name = models.CharField(_("College name"), blank=True, max_length=100)
    college_received_acceptance_letter = models.NullBooleanField(_("I have received an acceptance letter."), max_length=100)

    # PAGE 3: ESSAY
    essay = models.TextField(blank=True, null=True)
    
    # PAGE 4: ACTIVITIES
    # Academic awards / honors / Athletics / Clubs / Extracurriculars / Work Experience / Other
    activities = JSONListSchemaField(_("Activities"), help_text=_("Please list your main extracurricular activities and work experience below: Include the grade level of your participation. Feel free to attach a resume or a more complete list (on the upload documents page) to supplement this list."),name='activities', blank=True, null=True)

    # PAGE 5: UPLOAD FILES:
    file_resume = DocumentField(_("Please upload your resume if available."), blank=True, null=True)
    file_sat_scores = DocumentField(_("Please upload SAT scores if applicable."), blank=True, null=True)
    file_act_scores = DocumentField(_("Please upload ACT scores if applicable."), blank=True, null=True)
    file_transcript = DocumentField(_("Please upload your high school transcript."), blank=True, null=True)
    
    file_finaid_cost = DocumentField(_("Financial aid package / cost of attendance letter from the university"), blank=True, null=True)
    file_finaid_tuition = DocumentField(_("Tuition bill for applicant / other dependents if necessary"), blank=True, null=True)
    file_finaid_taxreturn = DocumentField(_("2016 tax return; 1040 along with supporting documentation"), blank=True, null=True)
    file_finaid_cssprofile = DocumentField(_("CSS profile report"), blank=True, null=True)
    file_finaid_additional = DocumentField(_("Any additional documents (optional)"), blank=True, null=True)
    
    # PAGE 6: FINANCIAL INFORMATION
    finaid_applying_for = models.NullBooleanField(_("Applying for financial aid?"), help_text=_("If you are applying for financial aid, you will be applying for the separate financial aid scholarship. Otherwise, you will be considered only for the merit scholarship."))
    finaid_income_parent = models.IntegerField(_("Total income of both parents/ guardians last year"),blank=True, null=True)
    finaid_income_student = models.IntegerField(_("Total income of student / applicant last year"),blank=True, null=True)
    finaid_list_dependents = JSONListSchemaField(_("List of dependents currently attending college"), blank=True, null=True)
    finaid_college_costs_applicant = models.IntegerField(_("Approximate college cost for applicant"), blank=True, null=True)
    finaid_college_costs_dependents = models.IntegerField(_("Approximate college cost for other dependents"), blank=True, null=True)
    finaid_expected_contribution = models.IntegerField(_("Expected financial contribution"), blank=True, null=True) # per year? todo

    # financial assistance from other sources
    finaid_scholarships_hope = JSONField(blank=True, null=True)
    finaid_scholarships_pell = JSONField(blank=True, null=True)
    finaid_scholarships_other = JSONField(blank=True, null=True)

    finaid_needs_statement = models.TextField(_("Please describe any unusual financial circumstances in your family not listed previously on your application. You may include any information that will be beneficial to the Indian American Scholarship committee."), blank=True, null=True)

    # submit page:
    signature = models.CharField(_("Signature"), max_length=101, blank=True, null=True)

    # form meta fields.
    date_created = models.DateField(null=True, blank=True)
    date_last_submitted = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=False, blank=False, default="2018")

    def __str__(self):
        return self.first_name + " " + self.last_name
    def getApplicantName(self):
        return self.first_name + " " + self.last_name
    getApplicantName.short_description = "Name"
    def getApplicationType(self):
        # Returns application type for display in admin.
        if self.finaid_applying_for is None:
            return "Unspecified"
        if not self.finaid_applying_for:
            return "Merit"
        else:
            return "Financial Aid"
    getApplicationType.short_description = "Type"
    def getSubmitted(self):
        return False if self.date_last_submitted is None else True
    getSubmitted.short_description = "Submitted"
    @classmethod
    def getFields(self, number):
        return self.pages[number]["fields"];
    @classmethod
    def getShouldSubmitAjax(self, number):
        if ("submitAjax" in self.pages[number]):
            return self.pages[number]["submitAjax"]
        return False
    @classmethod
    def getIsSubmitPage(self, number):
        if ("submitPage" in self.pages[number]):
            return self.pages[number]["submitPage"]
        return False