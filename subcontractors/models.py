from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.utils import timezone
from datetime import datetime

import misaka
from django import template
from projects.models import Project

# Subcontractors MODELS.PY file
# Create your models here.

class JobCategory(models.Model):
    jobcategory_name = models.CharField(max_length=264,unique=True, verbose_name="Name")
    class Meta:
        verbose_name_plural = "Job Categories"
    def __str__(self):
        return self.jobcategory_name
    def get_absolute_url(self):
        return reverse('subcontractors:job_categories_list')

class Subcontractor(models.Model):
    subcontractor_job_category = models.ForeignKey(JobCategory,related_name='category_sucontractors',on_delete=models.CASCADE, verbose_name="Category")
    subcontractor_name = models.CharField(max_length=264,unique=True, verbose_name="Name")
    subcontractor_location = models.CharField(max_length=264,unique=False, verbose_name="Location")
    subcontractor_phone_number = models.IntegerField(null=True, blank=True, verbose_name="Phone Number")
    subcontractor_contact_person = models.CharField(blank=True, max_length=264, verbose_name="Contact")
    subcontractor_description = models.CharField(max_length=264, blank=True,unique=False, verbose_name="Comment")
    def __str__(self):
        return self.subcontractor_name

class Job(models.Model):
    job_subcontractor = models.ForeignKey(Subcontractor,related_name='subcontractor_jobs',on_delete=models.CASCADE)
    job_project = models.ForeignKey(Project,related_name='project_jobs',on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory,related_name='job_category_jobs',on_delete=models.CASCADE)
    job_description = models.CharField(max_length=264,unique=False)
    job_status_choices = (
        ('Requested', 'Requested by subcontractor'),
        ('Received', 'Received from subcontractor'),
        ('Approved', 'Approved')
    )
    job_status = models.CharField(max_length=10, choices = job_status_choices, blank = False, default="Requested")
    job_created_date = models.DateTimeField(auto_now=True)
    job_requested_date = models.DateTimeField(default=datetime.now, blank=True)
    job_cost = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.job_project, self.job_category, self.job_description)
