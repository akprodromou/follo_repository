from django.urls import path
from subcontractors import views

app_name = 'subcontractors'
urlpatterns = [
    path('contacts/', views.contact_list.as_view(), name='contact_list'),
    path('add_jobcategory/', views.add_jobcategory.as_view(), name='add_jobcategory'),
    path('add_contact/', views.add_contact.as_view(), name='add_contact'),
    path('edit_contact/<int:pk>/', views.edit_contact.as_view(), name='edit_contact'),
    path('delete_contact/<int:pk>/', views.delete_contact.as_view(), name='delete_contact'),
]
