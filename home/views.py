from django.shortcuts import render
from django.db.models import Count
from holidays.models import Package
from django.conf import settings

# Create your views here.

def index(request):
    """A view to retun the index page"""
    holidays = []

    # https://stackoverflow.com/questions/9437726/how-to-get-the-value-of-a-variable-given-its-name-in-a-string
    for i in range(1, 7):
        name = f'settings.POPULAR_DESTINATION_{i}'
        holidays.append(eval(name))

    holidays = Package.objects.filter(name__in=holidays).annotate(num_reviews=Count('reviews'))
    template = 'home/index.html'
    context = {
        'holidays': holidays,
    }
    
    return render(request, template, context)