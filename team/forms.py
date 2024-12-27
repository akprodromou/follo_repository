from django import forms
from django.core import validators
from accounts.models import User
from team.models import Comment, Task, Worktime
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth import get_user_model
User = get_user_model()

class AddWorktimeForm(forms.ModelForm):
    class Meta:
        model = Worktime
        fields = '__all__'
        widgets = {
            'worktime_user': forms.HiddenInput(),
            'worktime_date': DatePickerInput(format='%d/%m/%Y'),
            }

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_task','comment_author','comment_text',)
        labels = {
            'comment_text': '',
        }
        widgets = {
            'comment_author': forms.HiddenInput(),
            'comment_task': forms.HiddenInput(),
            'comment_text': forms.Textarea(),
            }
