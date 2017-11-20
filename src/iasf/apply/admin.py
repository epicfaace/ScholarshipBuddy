# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Application
from django import forms
from django.utils.translation import ugettext_lazy as _

class ApplicationTypeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Application Type')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'applicationtype'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('merit', _('Merit')),
            ('financialaid', _('Financial Aid')),
            ('unspecified', _('Unspecified')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'merit':
            return queryset.filter(finaid_applying_for=False)
        if self.value() == 'financialaid':
            return queryset.filter(finaid_applying_for=True)
        if self.value() == 'neither':
            return queryset.filter(finaid_applying_for__isnull=True)

class ApplicationHasSubmittedFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Submitted?')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'submitted'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('y', _('Yes')),
            ('n', _('No')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        findNulls = False if self.value() == 'y' else 'n'
        return queryset.filter(date_last_submitted__isnull=findNulls)


class ApplicationModelForm(forms.ModelForm):
    pass

class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationModelForm
    list_filter = (ApplicationTypeListFilter, ApplicationHasSubmittedFilter,)
    list_display = ('getApplicantName', 'getApplicationType', 'home_city', 'date_last_submitted',)


admin.site.site_header = "IASF Scholarship Review Portal"
admin.site.register(Application, ApplicationAdmin)