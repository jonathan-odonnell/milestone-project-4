from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Package, Category, Country, Region
from django.db.models import Min
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import PackageForm, PriceFormset, ItineraryFormset


def category_holidays(request, category):
    """ A view to show all holidays in the category, including sorting and search queries """
    category = category.replace('-', ' ')
    category = get_object_or_404(Category, name__iexact=category)
    holidays = Package.objects.filter(
        category__name=category).annotate(min_price=Min('price__price'))
    countries = holidays.values_list(
        'country__name', flat=True).distinct().order_by('country__name')
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
            current_countries = request.POST['country'].replace(
                '_', ' ').split(',')
            holidays = holidays.annotate(lower_country=Lower('country__name')).filter(
                lower_country__in=current_countries)
            current_countries = Country.objects.annotate(lower_name=Lower('name')).filter(
                lower_name__in=current_countries).values_list('name', flat=True)

        # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
        holidays = Paginator(holidays, 12)
        page_number = request.POST['page']
        holidays = holidays.get_page(page_number)
        html = render_to_string(
            'holidays/includes/holidays.html', {'holidays': holidays, 'category': category})
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
    holidays = Package.objects.filter(
        country__region=destination).annotate(min_price=Min('price__price'))
    categories = holidays.values_list(
        'category__name', flat=True).distinct().order_by('category__name')
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
            current_categories = request.POST['category'].replace(
                '_', ' ').split(',')
            holidays = holidays.annotate(lower_category=Lower('category__name')).filter(
                lower_category__in=current_categories)
            current_categories = Category.objects.annotate(lower_name=Lower('name')).filter(
                lower_name__in=current_categories).values_list('name', flat=True)

        # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
        holidays = Paginator(holidays, 12)
        page_number = request.POST['page']
        holidays = holidays.get_page(page_number)
        html = render_to_string('holidays/includes/holidays.html',
                                {'holidays': holidays, 'destination': destination})
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


def holiday_details(request, slug, destination=None, category=None):
    """ A view to show individual holiday details """
    holiday = get_object_or_404(Package.objects
                                .annotate(min_price=Min('price__price')), slug=slug)

    if category:
        category = category.replace('-', ' ')
        related_holidays = Package.objects.exclude(name=holiday.name).annotate(
            lower_category=Lower('category__name'), min_price=Min('price__price'))
        related_holidays = related_holidays.filter(
            lower_category=category).order_by('?')[:4]

    else:
        destination = destination.replace('-', ' ')
        related_holidays = Package.objects.exclude(name=holiday.name).annotate(
            lower_region=Lower('country__region__name'), min_price=Min('price__price'))
        related_holidays = related_holidays.filter(
            lower_region=destination).order_by('?')[:4]

    context = {
        'holiday': holiday,
        'related_holidays': related_holidays,
        'category': category,
        'destination': destination
    }
    return render(request, 'holidays/holiday_details.html', context)


def add_holiday(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)

        if form.is_valid():
            holiday = form.save(commit=False)
            price_formset = PriceFormset(request.POST, instance=holiday)
            itinerary_formset = ItineraryFormset(request.POST, instance=holiday)

            if price_formset.is_valid() and itinerary_formset.is_valid():
                holiday.save()
                price_formset.save()
                itinerary_formset.save()
                messages.success(request, 'Successfully added holiday!')
                return redirect(reverse('destination_details', args=[holiday.country.region.slug, holiday.slug]))

        messages.error(
            request, 'Failed to add holiday. Please ensure the form is valid.')

    else:
        form = PackageForm()
        price_formset = PriceFormset()
        itinerary_formset = ItineraryFormset()

    template = 'holidays/add_holiday.html'
    context = {
        'form': form,
        'price_formset': price_formset,
        'itinerary_formset': itinerary_formset,
    }
    return render(request, template, context)


def edit_holiday(request, package):
    holiday = get_object_or_404(Package, slug=package)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=holiday)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated holiday!')
            return redirect(reverse('destination_details', args=[holiday.slug]))
        else:
            messages.error(
                request, 'Failed to update holiday. Please ensure the form is valid.')
    else:
        form = PackageForm(instance=holiday)

    template = 'holidays/edit_holiday.html'
    context = {
        'form': form,
        'holiday': holiday,
    }

    return render(request, template, context)


def delete_holiday(request, package):
    holiday = get_object_or_404(Package, slug=package)
    holiday.delete()
    messages.success(request, 'Holiday deleted!')
    return redirect(reverse('destinations'))
