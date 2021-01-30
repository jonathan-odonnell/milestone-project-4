from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('<int:holiday_id>', views.add_booking, name='add_booking'),
    path('update_guests/', views.update_guests, name='update_guests'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
]