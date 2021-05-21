from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST
from .models import NewsletterSignUp
from holidays.models import Package
from django.conf import settings

# Create your views here.


def index(request):
    """A view to retun the index page"""
    holidays = [
        settings.POPULAR_DESTINATION_1,
        settings.POPULAR_DESTINATION_2,
        settings.POPULAR_DESTINATION_3, 
        settings.POPULAR_DESTINATION_4,
        settings.POPULAR_DESTINATION_5,
        settings.POPULAR_DESTINATION_6,
    ]
    offers = [
        settings.OFFER_DESTINATION_1,
        settings.OFFER_DESTINATION_2,
        settings.OFFER_DESTINATION_3,
    ]

    holidays = Package.objects.filter(name__in=holidays)
    offers = Package.objects.filter(name__in=offers)

    template = 'home/index.html'
    context = {
        'holidays': holidays,
        'offers': offers,
    }

    return render(request, template, context)


@require_POST
def newsletter(request):
    """A view to add the customer's email to the newsletter sign ups database"""
    sign_up = NewsletterSignUp(email=request.POST['newsletter'])
    sign_up.save()

    return HttpResponse(200)
