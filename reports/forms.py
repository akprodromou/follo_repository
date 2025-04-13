from django import forms
from django.core import validators
from bootstrap_datepicker_plus import DatePickerInput
from .models import *
from django.utils.translation import gettext_lazy as _


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'report_issued_date': DatePickerInput(attrs={
                # 'class': 'form-control m-2',
                },format='%d/%m/%Y'),
        }

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = '__all__'
        widgets = {
            'action_notes': forms.Textarea(attrs={
                'class': 'form-control',
                }),
            'action_action': forms.Textarea(attrs={
                'class': 'form-control',
                }),
            'action_assignees': forms.SelectMultiple(attrs={
                'class': 'js-multiple form-control',
                'multiple': 'multiple',
                }),
            'action_date_deadline': DatePickerInput(attrs={
                # 'class': 'm-2',
                },format='%d/%m/%Y'),
        }
    field_order = [
        'action_notes',
        'action_action',
        'action_project',
        'action_owner',
        'action_assignees',
        'action_date_deadline',
        ]
