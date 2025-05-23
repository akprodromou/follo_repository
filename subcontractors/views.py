from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from bootstrap_datepicker_plus import DatePickerInput
from django.forms import BaseFormSet
from subcontractors.models import *
from subcontractors.forms import *

# Subcontractors VIEWS.PY

# Job category CRUD

class add_jobcategory(LoginRequiredMixin,generic.CreateView):
# class add_jobcategory(generic.CreateView):
    fields = ('jobcategory_name',)
    model = JobCategory
    template_name = 'subcontractors/add_jobcategory.html'

class edit_jobcategory(LoginRequiredMixin,generic.UpdateView):
# class edit_jobcategory(generic.UpdateView):
    fields = ('jobcategory_name',)
    model = JobCategory
    template_name = 'subcontractors/add_jobcategory.html'

class delete_jobcategory(LoginRequiredMixin,generic.DeleteView):
# class delete_jobcategory(generic.DeleteView):
    fields = ('jobcategory_name',)
    model = JobCategory
    template_name = 'subcontractors/add_jobcategory.html'

# Subcontractor CRUD

class add_contact(LoginRequiredMixin,generic.CreateView):
# class add_contact(generic.CreateView):
    fields = '__all__'
    model = Subcontractor
    template_name = 'subcontractors/add_contact.html'
    def get_success_url(self):
        return reverse('subcontractors:job_categories_list')

class edit_contact(LoginRequiredMixin,generic.UpdateView):
# class edit_contact(generic.UpdateView):
    fields = '__all__'
    model = Subcontractor
    template_name = 'subcontractors/edit_contact.html'
    def get_success_url(self):
        return reverse('subcontractors:job_categories_list')

class delete_contact(LoginRequiredMixin,generic.DeleteView):
# class delete_contact(generic.DeleteView):
    model = Subcontractor
    template_name = 'subcontractors/delete_contact.html'
    def get_success_url(self):
        return reverse('subcontractors:job_categories_list')

class contact_list(LoginRequiredMixin,generic.ListView):
# class contact_list(generic.ListView):
    model = Subcontractor
    template_name = 'subcontractors/contact_list.html'
