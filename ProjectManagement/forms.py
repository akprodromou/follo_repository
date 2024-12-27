from django import forms
from django.forms.widgets import HiddenInput
from bootstrap_datepicker_plus.widgets import DatePickerInput
from team.models import Task
from django.contrib.auth import get_user_model
User = get_user_model()

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'task_due_date': DatePickerInput(format='%d/%m/%Y'),
            'task_owner': HiddenInput(),
            'task_completion_date': HiddenInput(),
        }

class PasswordResetForm(forms.ModelForm):
    email = forms.CharField(label='')
    class Meta:
        fields = ('email',)
