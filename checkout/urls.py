from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<booking_number>/',
         views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('paypal/', views.paypal, name='paypal'),
    path('paypal/approve/', views.paypal_approve, name='paypal_approve'),
    path('wh/', webhook, name='webhook'),
]
