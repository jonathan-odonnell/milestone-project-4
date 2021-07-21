from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('.well-known/<path:path>',
         views.apple_pay_domain_association,
         name='apple_pay_domain_association'),
    path('google3dc647a21b4afb17.html',
         views.google_domain_verification,
         name='google_domain_verification')
]
