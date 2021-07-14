from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('.well-known/apple-developer-merchantid-domain-association/',
         views.apple_pay_domain_association,
         name='apple_pay_domain_association')
]
