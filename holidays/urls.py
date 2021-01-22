from django.urls import path
from . import views

urlpatterns = [
    path('<str:category>/', views.category_holidays, name='categories'),
    path('destinations/<str:destination>/', views.destination_holidays, name='destinations'),
]