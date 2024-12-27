from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2',)
    def __init__(self,*args,**kwargs):
        # invoke the superclass
        super().__init__(*args,**kwargs)
        # add an element
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email address'


class EditUserForm(forms.ModelForm):
    class Meta:
        fields = ('username', 'first_name','last_name','email', )
        model = get_user_model()
    def __init__(self,*args,**kwargs):
        # invoke the superclass
        super().__init__(*args,**kwargs)
        # add an element
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email address'
