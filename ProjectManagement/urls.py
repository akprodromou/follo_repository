"""ProjectManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index.as_view(), name='index'),
    path('search/', views.projectsearch.as_view(), name='projectsearch'),
    path('update_task_status/<int:pk>/', views.update_task_status, name='update_task_status'),
    path('add_task_index/<int:pk>/', views.add_task_index.as_view(), name='add_task_index'),
    # URL patterns for charts
    path('user_tasks_chart/', views.user_tasks_chart, name='user_tasks_chart'),
    path('team_tasks_category/', views.team_tasks_category, name='team_tasks_category'),
    # This will include all the login-registtration etc. URL patterns:
    path('accounts/', include('accounts.urls',namespace="accounts")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('projects/', include('projects.urls',namespace="projects")),
    path('subcontractors/', include('subcontractors.urls',namespace="subcontractors")),
    path('team/', include('team.urls',namespace="team")),
    path('reports/', include('reports.urls',namespace="reports")),
    path('api/search_autocomplete/', views.search_autocomplete, name='search_autocomplete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
