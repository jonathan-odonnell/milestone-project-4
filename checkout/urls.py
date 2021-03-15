from django.urls import path
from . import views
from .webhooks import stripe_webhook, paypal_webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<booking_number>',
         views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('get_profile/', views.get_profile, name='get_profile'),
    path('paypal/', views.paypal, name='paypal'),
    path('stripe-wh/', stripe_webhook, name='webhook'),
    path('paypal-wh/', paypal_webhook, name='paypal_webhook'),
]
