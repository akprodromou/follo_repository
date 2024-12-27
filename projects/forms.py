from django import forms
from django.core import validators
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import *
from django.contrib.auth.models import User



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'project_members': forms.SelectMultiple(attrs={
                'class': 'form-control  js-multiple',
                'multiple': 'multiple',
                }),
        }
