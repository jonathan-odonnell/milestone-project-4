from django.urls import path
from . import views

urlpatterns = [
    path('destinations/<slug:destination>/', views.destination_holidays, name='destinations'),
    path('destinations/<slug:destination>/<slug:slug>/', views.holiday_details, name='destination_details'),
    path('<str:category>/<slug:slug>/', views.holiday_details, name='category_details'),
    path('<slug:category>/', views.category_holidays, name='categories'),
]