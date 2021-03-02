from django.urls import path
from . import views

urlpatterns = [
    path('', views.extras, name='extras'),
    path('add/', views.add_extra, name='add_extra'),
    path('edit/<int:extra_id>/', views.edit_extra, name='edit_extra'),
    path('delete/<int:extra_id>/', views.delete_extra, name='delete_extra'),
]
