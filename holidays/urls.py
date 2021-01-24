from django.urls import path
from . import views

urlpatterns = [
    path('<str:category>/', views.category_holidays, name='categories'),
    path('destinations/<str:destination>/', views.destination_holidays, name='destinations'),
    path('details/<slug:slug>/', views.holiday_details, name='holiday_details'),
]