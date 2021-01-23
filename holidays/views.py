from django.shortcuts import render, get_object_or_404
from .models import Package, Category, Country, Region
from django.db.models import Min
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

def category_holidays(request, category):
    """ A view to show all holidays in the category, including sorting and search queries """
    category = category.replace('-', ' ')
    category=get_object_or_404(Category, name__iexact=category)
    holidays = Package.objects.filter(category__name=category).annotate(min_price=Min('price__price'))
    countries = holidays.values_list('country__name', flat=True).distinct().order_by('country__name')
    current_countries = None
    sort = None
    direction = None
    
    if request.method == 'POST':
        if 'sort' in request.POST:
            sort = request.POST['sort']
            if sort == 'price':
                sort = 'min_price'
            if 'direction' in request.POST:
                direction = request.POST['direction']
                if direction == 'desc':
                    sort = f'-{sort}'
                    
                holidays = holidays.order_by(sort)

        if 'country' in request.POST:
            current_countries = request.POST['country'].replace('_', ' ').split(',')
            holidays = holidays.annotate(lower_country=Lower('country__name')).filter(lower_country__in=current_countries)
            current_countries = Country.objects.annotate(lower_name=Lower('name')).filter(lower_name__in=current_countries).values_list('name', flat=True)

        # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
        holidays = Paginator(holidays, 12)
        page_number = request.POST['page']
        holidays = holidays.get_page(page_number)
        html = render_to_string('holidays/includes/holidays.html', {'holidays': holidays})
        return JsonResponse({'holidays': html, 'pages': holidays.paginator.num_pages})
    
    else:
        holidays = Paginator(holidays, 12)
        page_number = None
        holidays = holidays.get_page(page_number)
        context = {
            'category': category,
            'countries': countries,
            'holidays': holidays,
        }

        return render(request, 'holidays/categories.html', context)

def destination_holidays(request, destination):
    """ A view to show holidays in the destination, including sorting and search queries """
    destination = destination.replace('-', ' ')
    destination = get_object_or_404(Region, name__iexact=destination)
    holidays = Package.objects.filter(country__region=destination).annotate(min_price=Min('price__price'))
    categories = holidays.values_list('category__name', flat=True).distinct().order_by('category__name')
    current_categories = None
    sort = None
    direction = None

    if request.method == 'POST':
        if 'sort' in request.POST:
            sort = request.POST['sort']
            if sort == 'price':
                sort = 'min_price'
            if 'direction' in request.POST:
                direction = request.POST['direction']
                if direction == 'desc':
                    sort = f'-{sort}'

            holidays = holidays.order_by(sort)

        if 'category' in request.POST:
            current_categories = request.POST['category'].replace('_', ' ').split(',')
            holidays = holidays.annotate(lower_category=Lower('category__name')).filter(lower_category__in=current_categories)
            current_categories = Category.objects.annotate(lower_name=Lower('name')).filter(lower_name__in=current_categories).values_list('name', flat=True)

        # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
        holidays = Paginator(holidays, 12)
        page_number = request.POST['page']
        holidays = holidays.get_page(page_number)
        html = render_to_string('holidays/includes/holidays.html', {'holidays': holidays})
        return JsonResponse({'holidays': html, 'pages': holidays.paginator.num_pages})

    else:
        holidays = Paginator(holidays, 12)
        page_number = None
        holidays = holidays.get_page(page_number)
        context = {
            'destination': destination,
            'categories': categories,
            'holidays': holidays,
        }

        return render(request, 'holidays/destinations.html', context)

def holiday_details(request, slug):
    """ A view to show individual holiday details """

    holiday = get_object_or_404(Package.objects
        .annotate(min_price=Min('price__price')), slug=slug)

    context = {
        'holiday': holiday,
    }
    return render(request, 'holidays/holiday_details.html', context)
