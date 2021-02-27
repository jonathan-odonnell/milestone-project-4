from django.urls import path
from . import views

urlpatterns = [
    path('', views.extras, name='extras'),
]
