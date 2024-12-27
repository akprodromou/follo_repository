from django.urls import path
from team import views

app_name = 'team'
urlpatterns = [
    path('', views.users_list.as_view(), name='users_list'),
    path('<int:pk>/', views.user_detail.as_view(), name='user_detail'),
    path('add_task_user/<int:pk>/', views.add_task_user.as_view(), name='add_task_user'),
    path('update_task_status/<int:pk>/', views.update_task_status, name='update_task_status'),
    path('edit_task_user/<int:pk>/', views.edit_task_user.as_view(), name='edit_task_user'),
    path('tasks/<int:pk>/', views.task_detail.as_view(), name='task_detail'),
    path('delete_task_user/<int:pk>/', views.delete_task_user.as_view(), name='delete_task_user'),
    path('worktime_list_user/<int:pk>/', views.worktime_list_user.as_view(), name='worktime_list_user'),
    path('worktime_history_user/<int:pk>/', views.worktime_history_user.as_view(), name='worktime_history_user'),
    path('add_worktime_user/<int:pk>/', views.add_worktime_user, name='add_worktime_user'),
    path('edit_worktime_user/<int:pk>/', views.edit_worktime_user.as_view(), name='edit_worktime_user'),
    path('delete_worktime_user/<int:pk>/', views.delete_worktime_user.as_view(), name='delete_worktime_user'),
    path('user_task_history/<int:pk>/', views.user_task_history.as_view(), name='user_task_history'),
    path('team_activity/', views.team_activity.as_view(), name='team_activity'),
    path('user_hours_graph/<int:pk>/', views.user_hours_graph, name='user_hours_graph'),
    path('add_worktime_task/<int:pk>/', views.add_worktime_task, name='add_worktime_task'),
]
