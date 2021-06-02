from functools import wraps
from django.shortcuts import HttpResponse, get_object_or_404
from .models import Package, Category, Region
from django.db.models.functions import Lower
from django.core.paginator import Paginator

def superuser_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse(403)
        return function(request, *args, **kwargs)
    return wrap


def get_holidays(request, category=None, destination=None):
    countries = None
    categories = None
    sort = None
    direction = None
    current_sorting = None
    current_categories = None
    current_countries = None

    if category:
        category = get_object_or_404(Category, slug=category)
        holidays = Package.objects.filter(category=category)
        countries = holidays.values_list(
            'country__name', flat=True).distinct().order_by('country__name')

    elif destination:
        destination = get_object_or_404(Region, slug=destination)
        holidays = Package.objects.filter(region=destination)
        categories = holidays.values_list(
            'category__name', flat=True).distinct().order_by('category__name')

    else:
        holidays = Package.objects.filter(offer=True)
        categories = holidays.values_list(
            'category__name', flat=True).distinct().order_by('category__name')

    if request.GET:
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sortkey = sort
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            holidays = holidays.order_by(sortkey)
            current_sorting = f'{sort}_{direction}'

        if 'categories' in request.GET:
            current_categories = request.GET['categories'].replace(
                '_', ' ').split(',')
            holidays = holidays.annotate(lower_category=Lower('category__name')).filter(
                lower_category__in=current_categories)

        if 'countries' in request.GET:
            current_countries = request.GET['countries'].replace(
                '_', ' ').split(',')
            holidays = holidays.annotate(lower_country=Lower('country__name')).filter(
                lower_country__in=current_countries)

    paginated_holidays = Paginator(holidays, 12)
    page_number = request.GET.get('page')
    holidays = paginated_holidays.get_page(page_number)

    response = {
        'holidays': holidays,
        'category': category,
        'destination': destination,
        'current_sorting': current_sorting,
        'countries': countries,
        'current_countries': current_countries,
        'categories': categories,
        'current_categories': current_categories,
    }

    return response
