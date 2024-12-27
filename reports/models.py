from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
import datetime
from django import template
from projects.models import Project

User = get_user_model()

class Report(models.Model):
    report_issued_date =  models.DateField(unique=False, default=datetime.date.today,verbose_name='Report date')
    class Meta:
        ordering = ['-report_issued_date']
    def __str__(self):
        return str(self.report_issued_date)

class Action(models.Model):
    action_report = models.ForeignKey(Report,related_name='report_actions',on_delete=models.CASCADE)
    action_project = models.ForeignKey(Project,related_name='project_reports',on_delete=models.CASCADE)
    action_owner = models.ForeignKey(User,related_name='user_reports',on_delete=models.CASCADE)
    action_notes = models.TextField(blank=False,verbose_name='Issues/Notes')
    action_action = models.TextField(blank=False,verbose_name='Actions')
    action_assignees = models.ManyToManyField(User,verbose_name='Assigned to',
        blank=False, related_name='user_report_actions')
    action_date_deadline =  models.DateField(blank=False,verbose_name='Date',unique=False)
    class Meta:
        ordering = ['-action_report']
    def __str__(self):
        return str(self.action_action)
