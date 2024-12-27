from django.contrib import admin
from .models import Project, ProjectCategory

# Register your models here.
admin.site.register(ProjectCategory)
admin.site.register(Project)
