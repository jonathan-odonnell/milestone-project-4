from django.shortcuts import render, get_object_or_404
from .models import Package, Category, Country, Region
from django.db.models import Min

def category_holidays(request, category):
    """ A view to show all holidays, including sorting and search queries """
    category = category.replace('-', ' ')
    category=get_object_or_404(Category, name__iexact=category)
    holidays = Package.objects.filter(category__name=category).annotate(min_price=Min('price__price'))
    countries = holidays.values_list('country__name', flat=True).distinct().order_by('country__name')

    context = {
        'category': category,
        'countries': countries,
        'holidays': holidays,
    }

    return render(request, 'holidays/categories.html', context)

def destination_holidays(request, destination):
    """ A view to show all holidays, including sorting and search queries """
    destination = destination.replace('-', ' ')
    destination = get_object_or_404(Region, name__iexact=destination)
    holidays = Package.objects.filter(country__region=destination).annotate(min_price=Min('price__price'))
    categories = holidays.values_list('category__name', flat=True).distinct().order_by('category__name')

    context = {
        'destination': destination,
        'categories': categories,
        'holidays': holidays,
    }

    return render(request, 'holidays/destinations.html', context)
