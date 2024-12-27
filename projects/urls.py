from django.urls import path
from projects import views

app_name = 'projects'
urlpatterns = [
    path('', views.project_categories_list.as_view(), name='project_categories_list'),
    path('<int:projectcategory_number>/', views.project_category.as_view(), name='project_category'),
    path('projects/<int:pk>/', views.project_detail.as_view(), name='project_detail'),
    path('add_project/<int:pk>/', views.add_project.as_view(), name='add_project'),
    path('add_projectcategory/', views.add_project_category.as_view(), name='add_project_category'),
    path('edit_project/<int:pk>/', views.edit_project.as_view(), name='edit_project'),
    path('add_job_project/<int:pk>/', views.add_job_project.as_view(), name='add_job_project'),
    path('add_task_project/<int:pk>/', views.add_task_project.as_view(), name='add_task_project'),
    path('join_project/<int:pk>/', views.join_project.as_view(), name='join_project'),
    path('leave_project/<int:pk>/', views.leave_project.as_view(), name='leave_project'),
    path('project_task_history/<int:pk>/', views.project_task_history.as_view(), name='project_task_history'),
    path('busiest_projects/', views.busiest_projects, name='busiest_projects'),
    path('busiest_project_categories/', views.busiest_project_categories, name='busiest_project_categories'),
    path('project_hours_graph/<int:pk>/', views.project_hours_graph, name='project_hours_graph'),
    path('add_worktime_project/<int:pk>/', views.add_worktime_project, name='add_worktime_project'),
    path('add_worktime_modal/<int:pk>/', views.add_worktime_modal, name='add_worktime_modal'),
]
