from django.contrib import admin
from .models import Job, Subcontractor, JobCategory

# Register your models here.
admin.site.register(Job)
admin.site.register(JobCategory)
admin.site.register(Subcontractor)
