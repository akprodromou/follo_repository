from django.contrib import admin
from .models import Task, Comment, Worktime, UserProfile

class UserProfileInline(admin.TabularInline):
    model = UserProfile

# Register your models here.
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Worktime)
admin.site.register(UserProfile)
