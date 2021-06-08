from django.urls import path
from . import views

urlpatterns = [
    path('', views.extras, name='extras'),
    path('add/', views.add_extra, name='add_extra'),
    path('edit/<slug:extra>/', views.edit_extra, name='edit_extra'),
    path('delete/<slug:extra>/', views.delete_extra, name='delete_extra'),
]
