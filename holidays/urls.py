from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.holidays, name='offers'),
    path('offers/<slug:slug>/', views.holiday_details, name='offer_details'),
    path('destinations/<slug:destination>/', views.holidays, name='destinations'),
    path('destinations/<slug:destination>/<slug:slug>/', views.holiday_details, name='destination_details'),
    path('review/<slug:package>/', views.review, name='review'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<slug:package>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<slug:package>/', views.delete_holiday, name='delete_holiday'),
    path('<slug:category>/', views.holidays, name='categories'),
    path('<str:category>/<slug:slug>/', views.holiday_details, name='category_details'),
]