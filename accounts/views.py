from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from . import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic

User = get_user_model()

# Create your views here.
class signup(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/signup.html'

class edit_user(LoginRequiredMixin,generic.UpdateView):
    model = User
    form_class = forms.EditUserForm
    template_name = 'accounts/edit_user.html'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk':self.kwargs['pk']})

class delete_user(LoginRequiredMixin,generic.DeleteView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('index')
    template_name = 'accounts/delete_user.html'
