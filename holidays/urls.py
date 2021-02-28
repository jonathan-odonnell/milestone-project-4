from django.urls import path
from . import views

urlpatterns = [
    path('destinations/<slug:destination>/', views.destination_holidays, name='destinations'),
    path('destinations/<slug:destination>/<slug:slug>/', views.holiday_details, name='destination_details'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<slug:package>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<slug:package>/', views.delete_holiday, name='delete_holiday'),
    path('<str:category>/<slug:slug>/', views.holiday_details, name='category_details'),
    path('<slug:category>/', views.category_holidays, name='categories'),
]