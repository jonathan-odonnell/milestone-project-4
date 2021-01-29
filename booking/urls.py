from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('<int:holiday_id>', views.add_booking, name='add_booking')
]