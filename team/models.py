from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
import datetime

import misaka
from django import template
from projects.models import Project

User = get_user_model()

# Team MODELS.PY file
# Create your models here.


class Task(models.Model):
    task_project = models.ForeignKey(Project,related_name='project_tasks',on_delete=models.CASCADE)
    task_description = models.CharField(max_length=264,unique=False)
    task_description_html = models.TextField(editable=False)
    task_owner = models.ForeignKey(User,related_name='user_tasks',on_delete=models.CASCADE)
    task_asignee = models.ForeignKey(User,related_name='assigned_tasks',on_delete=models.CASCADE, verbose_name='Assign task to')
    task_status_choices = (
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    )
    task_status = models.CharField(max_length=30, choices = task_status_choices, blank = False, default="Pending")
    task_creation_date = models.DateTimeField(auto_now=True)
    task_due_date = models.DateField()
    task_completion_date = models.DateTimeField(null=True, blank=True)
    def is_past_due(self):
        return self.task_due_date < datetime.date.today()
    def is_close_due(self):
        return self.task_due_date >= datetime.date.today() and self.task_due_date < datetime.date.today() + datetime.timedelta(days=5)
    def is_far_due(self):
        return self.task_due_date > datetime.date.today() + datetime.timedelta(days=5)
    def check_status_pending(self):
        return self.task_status == 'Pending'
    def viewed_comments(self):
        return self.task_comment.filter(comment_viewed=True)
    def save(self,*args,**kwargs):
        self.task_description_html = misaka.html(self.task_description)
        super().save(*args,**kwargs)
    class Meta:
        ordering = ['task_due_date']
    def __str__(self):
        return '{0} - {1}'.format(self.task_project, self.task_description)

class UserProfile(models.Model):
    userprofile_user = models.ForeignKey(User,on_delete=models.CASCADE)
    userprofile_photo = models.ImageField(null=True,blank=True,upload_to='uploads/', height_field=None, width_field=None)
    userprofile_position = models.CharField(max_length=20, null=False)
    userprofile_projects = models.ForeignKey(Project,related_name='user_projects',on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    comment_task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='task_comment')
    comment_author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created_date = models.DateTimeField(auto_now=True)
    comment_viewed = models.BooleanField(default=False)
    def viewed(self):
        self.comment_viewed = True
        self.save()
    class Meta:
        ordering = ['comment_created_date']
    def __str__(self):
        return self.comment_text
    def get_absolute_url(self):
        return reverse('team:task_detail', kwargs={'pk':self.comment_task.pk})

class Worktime(models.Model):
    worktime_task = models.ForeignKey(Task,related_name='task_time',on_delete=models.CASCADE)
    worktime_user = models.ForeignKey(User,related_name='user_time',on_delete=models.CASCADE)
    worktime_date = models.DateField(unique=False, default=datetime.date.today)
    worktime_hour = models.FloatField(unique=False, verbose_name='Hours')
    class Meta:
        ordering = ['-worktime_date']
    def __str__(self):
        return str(self.worktime_hour)
    def get_absolute_url(self):
        return reverse('team:task_detail', kwargs={'pk':self.comment_task.pk})
