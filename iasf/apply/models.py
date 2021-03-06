# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from .fields import JSONListSchemaField, DocumentField
from .validators import MaxWordsValidator
from django.forms import widgets

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
                ("High School information", {"fields": (
                    "hs_name", "hs_address_1", "hs_address_2", "hs_city", "hs_state", "hs_zip_code")
                }),
                ("High school counselor information", {"fields": ("hs_counselor_first_name", "hs_counselor_middle_name", "hs_counselor_last_name",
                    "hs_counselor_email")
                }),
                ("Grades and test scores", {"fields": (
                    "hs_gpa", "hs_class_rank","hs_class_size")
                }),
                #("SAT / ACT scores", {"fields": (
                ("scores_sat_reading","scores_sat_math","scores_sat_writing","scores_sat_total",),
                ("scores_act_reading","scores_act_math","scores_act_science","scores_act_writing","scores_act_composite",),
                ("scores_ap")
                ,
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
            "financialOnly": True,
            "fields": (
                ("Income", {"fields": (
                    "finaid_income_parent", "finaid_income_student",)
                }),
                ("finaid_list_dependents",),
                ("College costs", {"fields": (
                    "finaid_college_costs_applicant", "finaid_college_costs_dependents", "finaid_expected_contribution")
                }),
                ("Scholarships", {"fields": (
                    "finaid_scholarships_hope_eligible",
                    "finaid_scholarships_hope_amount",
                    "finaid_scholarships_hope_duration",)
                }),
                (   "finaid_scholarships_pell_eligible",
                    "finaid_scholarships_pell_amount",
                    "finaid_scholarships_pell_duration",),
                (   "finaid_scholarships_other",),
                ("Financial Needs Statement", {"fields": (
                    "finaid_needs_statement",)
                }),
            )
        },
        {
            "name": "Upload Files - Academic",
            "submitAjax": True,
            "fields": (
                ("Academic", {"fields": (
                    #"file_resume",)
                )
                }),
                ("file_transcript",),
                ("file_sat_scores",),
                ("file_act_scores",),
            )
        },
        {
            "name": "Upload Files - Financial Aid",
            "submitAjax": True,
            "financialOnly": True,
            "fields": (
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
                    "where_heard",)
                }),
                ("signature",)
            )
        }
    ]
    CLAIM_INDIAN_DESCENT_CHOICES = (
        (1, _("Maternal grandparents")),
        (2, _("Paternal grandparents"))
    )
    WHERE_HEARD_CHOICES = (
        (1, _("Friend/Family")),
        (2, _("Guidance counselor")),
        (3, _("Khabar magazine")),
        (4, _("Internet search")),
        (5, _("Other"))
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #todo: blank=False
    finaid_applying_for = models.BooleanField(_("Applying for financial aid?"), help_text=_("If you are applying for financial aid, you will be applying for the separate financial aid scholarship. Otherwise, you will be considered only for the merit scholarship."))

    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    phone_home = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name="Home Phone") # validators should be a list
    phone_mobile = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name="Mobile Phone") # validators should be a list
    claim_indian_descent = models.IntegerField(null=True, blank=False, choices=CLAIM_INDIAN_DESCENT_CHOICES, verbose_name="Claim to Indian descent")
    
    home_address_1 = models.CharField(_("Address Line 1"), max_length=128, blank=False)
    home_address_2 = models.CharField(_("Address Line 2"), max_length=128, blank=True)
    home_city = models.CharField(_("City"), max_length=64, default="", blank=False)
    home_state = models.CharField(_("State"), max_length=2, default="GA", blank=False) # todo disabled
    home_zip_code = models.CharField(_("Zip Code"), max_length=5, default="", blank=False)

    parent_first_name = models.CharField(max_length=50, blank=False)
    parent_middle_name = models.CharField(max_length=50, blank=True)
    parent_last_name = models.CharField(max_length=50, blank=False)

    # second page:
    hs_name = models.CharField(max_length=100, blank=False, verbose_name="HS Name")
    
    hs_address_1 = models.CharField(_("Address Line 1"), max_length=128, blank=False)
    hs_address_2 = models.CharField(_("Address Line 2"), max_length=128, blank=True)
    hs_city = models.CharField(_("City"), max_length=64, default="", blank=False)
    hs_state = models.CharField(_("State"), max_length=2, default="GA", blank=False) # todo disabled
    hs_zip_code = models.CharField(_("Zip Code"), max_length=5, default="", blank=False)
    
    hs_counselor_first_name = models.CharField(max_length=50, blank=True, verbose_name="Counselor first name")
    hs_counselor_middle_name = models.CharField(max_length=50, blank=True, verbose_name="Middle name")
    hs_counselor_last_name = models.CharField(max_length=50, blank=True, verbose_name="Last name")
    hs_counselor_email = models.EmailField(blank=True, verbose_name="Email")

    hs_gpa = models.DecimalField(_("HS GPA (100 or 4.0 scale)"), blank=True, null=True, max_digits=3, decimal_places = 1)
    hs_class_rank = models.IntegerField(null=True, blank=True,verbose_name="HS Class Rank")
    hs_class_size = models.IntegerField(null=True, blank=True,verbose_name="HS Class Size")

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

    scores_ap = JSONListSchemaField(_("AP Exams Taken"), schema="scores_ap", blank=True, null=True)

    college_name = models.CharField(_("College name"), blank=True, max_length=100)
    college_received_acceptance_letter = models.NullBooleanField(_("I have received an acceptance letter."))

    # PAGE 3: ESSAY
    essay = models.TextField(
        _("Essay (500 words max)"),
        help_text=_("Tell us something, like a personal experience, that's not evident from your application. This is an opportunity to show us who you are."),
        blank=False,
        null=True,
        validators=[MaxWordsValidator(500)])
    
    # PAGE 4: ACTIVITIES
    # Academic awards / honors / Athletics / Clubs / Extracurriculars / Work Experience / Other
    activities = JSONListSchemaField(_("Activities"), help_text=_("Please list your main extracurricular activities and work experience below: Include the grade level of your participation. Feel free to attach a resume or a more complete list (on the upload documents page) to supplement this list."),name='activities', blank=True, null=True)

    # PAGE 5: UPLOAD FILES:
    # file_resume = DocumentField(_("Please upload your resume if available."), blank=True, null=True)
    file_sat_scores = DocumentField(_("Please upload SAT scores if applicable."), blank=True, null=True)
    file_act_scores = DocumentField(_("Please upload ACT scores if applicable."), blank=True, null=True)
    file_transcript = DocumentField(
        _("Please upload your high school transcript."),
        help_text=_("Additionally, please send either a sealed paper copy to Rajesh Kurup (2137 Wisteria Way Atlanta GA 30317) or email an electronic copy from your guidance counselor to info@iasf.org."),
        blank=True, null=True)
    
    file_finaid_cost = DocumentField(_("Financial aid package / cost of attendance letter from the university"), blank=True, null=True)
    file_finaid_tuition = DocumentField(_("Tuition bill for applicant / other dependents if necessary"), blank=True, null=True)
    file_finaid_taxreturn = DocumentField(_("2016 tax return; 1040 along with supporting documentation"), blank=True, null=True)
    file_finaid_cssprofile = DocumentField(_("CSS profile report"), blank=True, null=True)
    file_finaid_additional = DocumentField(_("Any additional documents (optional)"), blank=True, null=True)
    
    # PAGE 6: FINANCIAL INFORMATION
    finaid_income_parent = models.IntegerField(_("Total income of both parents/ guardians last year"),blank=True, null=True)
    finaid_income_student = models.IntegerField(_("Total income of student / applicant last year"),blank=True, null=True)
    finaid_list_dependents = JSONListSchemaField(_("List of dependents currently attending college"), blank=True, null=True)
    finaid_college_costs_applicant = models.IntegerField(_("Approximate college cost for applicant"), blank=True, null=True)
    finaid_college_costs_dependents = models.IntegerField(_("Approximate college cost for other dependents"), blank=True, null=True)
    finaid_expected_contribution = models.IntegerField(_("Expected financial contribution"), blank=True, null=True) # per year? todo

    # financial assistance from other sources
    finaid_scholarships_hope_eligible = models.NullBooleanField(_("Eligible for HOPE Scholarship?"))
    finaid_scholarships_hope_amount = models.IntegerField(_("HOPE Annual Amount"), blank=True, null=True)
    finaid_scholarships_hope_duration = models.CharField(_("HOPE Expected Duration"), blank=True, null=True, max_length=20)
    finaid_scholarships_pell_eligible = models.NullBooleanField(_("Eligible for HOPE Scholarship?"))
    finaid_scholarships_pell_amount = models.IntegerField(_("Pell Annual Amount"), blank=True, null=True)
    finaid_scholarships_pell_duration = models.CharField(_("Pell Expected Duration"), blank=True, null=True, max_length=20)
    finaid_scholarships_other = JSONListSchemaField(_("Financial assistance from other sources"),blank=True, null=True)

    finaid_needs_statement = models.TextField(_("Please describe any unusual financial circumstances in your family not listed previously on your application. You may include any information that will be beneficial to the Indian American Scholarship committee."), blank=True, null=True)

    # submit page:
    where_heard = models.IntegerField(null=True, blank=False, choices=WHERE_HEARD_CHOICES, verbose_name="Where did you hear about the IASF scholarship program?")
    signature = models.CharField(_("Signature"), max_length=101, blank=True, null=True, help_text=_(""))

    # form meta fields.
    date_created = models.DateField(null=True, blank=True)
    date_last_modified = models.DateField(null=True, blank=True)
    date_last_submitted = models.DateField(null=True, blank=True)
    submitted = models.BooleanField(default=False, editable=False)
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
        fields = self.pages[number]["fields"]
        return fields
    @classmethod
    def getPages(self):
        """ Get pages. """
        pages = self.pages
        return pages
    @classmethod
    def isSubmitPage(self, number):
        """Is it a submit page? Then a different form should be used.
        """
        return number == len(self.pages) - 1
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
    def clean(self):
        return super(Application, self).clean()