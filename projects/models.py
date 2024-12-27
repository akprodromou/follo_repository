from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
import misaka
from django import template

# Project MODELS.PY file

User = get_user_model()
register = template.Library()

class ProjectCategory(models.Model):
    projectcategory_number = models.IntegerField(unique=True)
    projectcategory_name = models.CharField(max_length=264,unique=True)
    projectcategory_name_html = models.TextField(editable=False,default='',blank=True)
    # projectcategory_projects = models.ManyToManyField(Project, through='ProjectCategoryProject')
    def __str__(self):
        return '{0} - {1}'.format(self.projectcategory_number, self.projectcategory_name)
    def save(self,*args,**kwargs):
        self.projectcategory_name_html = misaka.html(self.projectcategory_name)
        super().save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse('projects:project_categories_list')
    class Meta:
        # verbose_name_plural = "Project Categories"
        ordering = ['projectcategory_number']
    @property
    def user_colors(self):
        return len(str(self))*40%255, 'Hi'


class Project(models.Model):
    project_category = models.ForeignKey(ProjectCategory,related_name='category_projects',on_delete=models.CASCADE)
    project_number = models.IntegerField(unique=True)
    project_name = models.CharField(max_length=264,unique=True)
    project_stage_choices = (
        ('Concept Design', 'CD - Concept Design'),
        ('Schematic Design', 'SD - Schematic Design'),
        ('Design Development', 'DD - Design Development'),
        ('Issued for Construction', 'IFC - Issued for Construction'),
        ('Closed', 'Closed'),
    )
    project_stage = models.CharField(max_length=30, choices = project_stage_choices, blank=False, default="CD")
    project_creator = models.ForeignKey(User,related_name="project_creator",on_delete=models.CASCADE)
    project_members = models.ManyToManyField(User,related_name="user_member_projects")
    project_delivery_date = models.DateField()
    project_status_choices = (
        ('On time', 'On time'),
        ('Delayed', 'Delayed'),
    )
    project_status = models.CharField(max_length=30, choices = project_status_choices, blank=False, default="On time")
    def close_project(self):
        self.project_stage = 'Closed'
        self.save()
    def __str__(self):
        return '{0} - {1}'.format(self.project_number, self.project_name)
    class Meta:
        unique_together = ('project_number','project_creator')
        ordering = ['project_number']
    def save(self,*args,**kwargs):
        self.project_name_html = misaka.html(self.project_name)
        super().save(*args,**kwargs)
