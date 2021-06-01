from django.urls import path
from . import views

urlpatterns = [
    path('', views.flights, name='flights'),
    path('filter/', views.filter_flights, name='filter_flights'),
    path('airports//<int:holiday_id>/', views.airports, name='airports'),
    path('add/', views.add_flight, name='add_flight'),
    path('edit/<flight_number>/', views.edit_flight, name='edit_flight'),
    path('delete/<flight_number>/', views.delete_flight, name='delete_flight'),
]