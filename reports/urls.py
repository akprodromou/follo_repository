from django.urls import path
from reports import views

app_name = 'reports'
urlpatterns = [
    path('', views.reports_list.as_view(), name='reports_list'),
    path('add_report', views.add_report, name='add_report'),
    path('edit_report/<int:pk>/', views.edit_report, name='edit_report'),
    path('delete_report/<int:pk>/', views.delete_report.as_view(), name='delete_report'),
]
