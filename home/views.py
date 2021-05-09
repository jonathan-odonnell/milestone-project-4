from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import NewsletterSignUp
from holidays.models import Package
from django.conf import settings

# Create your views here.


def index(request):
    """A view to retun the index page"""
    holidays = []
    offers = []

    # https://stackoverflow.com/questions/9437726/how-to-get-the-value-of-a-variable-given-its-name-in-a-string
    for i in range(1, 7):
        name = f'settings.POPULAR_DESTINATION_{i}'
        holidays.append(eval(name))

    for i in range(1, 4):
        name = f'settings.OFFER_DESTINATION_{i}'
        offers.append(eval(name))

    holidays = Package.objects.filter(
        name__in=holidays).annotate(num_reviews=Count('reviews'))
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
