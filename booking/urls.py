from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('<holiday_id>/', views.add_booking, name='add_booking'),
    path('update_guests/', views.update_guests, name='update_guests'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('add_extra/<extra_id>/', views.add_extra, name='add_extra'),
    path('update_extra/<extra_id>/', views.update_extra, name='update_extra'),
    path('remove_extra/<extra_id>/', views.remove_extra, name='remove_extra'),
]