from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('bookings/', views.bookings, name='bookings'),
    path('bookings/<booking_number>', views.booking_details, name='booking_details'),
]