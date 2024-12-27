from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('edit_user/<int:pk>/', views.edit_user.as_view(), name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user.as_view(), name='delete_user'),
]
