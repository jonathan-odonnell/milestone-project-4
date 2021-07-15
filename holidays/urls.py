from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.holidays, name='offers'),
    path('filter/offers/', views.holidays, name='filter_offers'),
    path('offers/<slug:package>/', views.holiday_details,
         name='offer_details'),
    path('destinations/<slug:destination>/',
         views.holidays, name='destinations'),
    path('filter/destinations/<slug:destination>/',
         views.holidays, name='filter_destinations'),
    path('destinations/<slug:destination>/<slug:package>/',
         views.holiday_details, name='destination_details'),
    path('review/<slug:package>/', views.review, name='review'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<slug:package>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<slug:package>/', views.delete_holiday,
         name='delete_holiday'),
    path('<slug:category>/', views.holidays, name='categories'),
    path('filter/<slug:category>/', views.holidays, name='filter_categories'),
    path('<str:category>/<slug:package>/',
         views.holiday_details, name='category_details'),
]
