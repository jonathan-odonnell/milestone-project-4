from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<booking_number>',
         views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
    path('get_profile/', views.get_profile, name='get_profile'),
    path('create-paypal-transaction/', views.create_paypal_transaction, name='create_paypal_transaction'),
]
