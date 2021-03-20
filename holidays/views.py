from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Package, Category, Country, Region
from flights.models import Flight
from django.db.models import Min
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PackageForm, PriceFormset, ItineraryFormset
from .utlis import superuser_required


def holidays(request, category=None, destination=None):
    """ A view to show all holidays for the category or destination, including sorting and search queries """
    countries = None
    categories = None
    current_categories = None
    current_countries = None
    sort = None
    direction = None

    if category == 'offers':
        category = get_object_or_404(Category, slug=category)
        holidays = Package.objects.filter(
            offer=True).annotate(min_price=Min('price__price'))
        categories = holidays.values_list(
            'category__name', flat=True).distinct().order_by('category__name')

    elif category:
        category = get_object_or_404(Category, slug=category)
        holidays = Package.objects.filter(
            category=category).annotate(min_price=Min('price__price'))
        countries = holidays.values_list(
            'country__name', flat=True).distinct().order_by('country__name')

    else:
        destination = get_object_or_404(Region, slug=destination)
        holidays = Package.objects.filter(
            country__region=destination).annotate(min_price=Min('price__price'))
        categories = holidays.values_list(
            'category__name', flat=True).distinct().order_by('category__name')

    if request.GET:
        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'price':
                sort = 'min_price'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort = f'-{sort}'

                holidays = holidays.order_by(sort)

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

        # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
        holidays = Paginator(holidays, 12)
        page_number = request.GET['page']
        holidays = holidays.get_page(page_number)
        html = render_to_string(
            'holidays/includes/holiday_cards.html', {'holidays': holidays, 'category': category, 'destination': destination})
        return JsonResponse({'holidays': html})

    else:
        holidays = Paginator(holidays, 12)
        page_number = None
        holidays = holidays.get_page(page_number)
        context = {
            'category': category,
            'destination': destination,
            'categories': categories,
            'countries': countries,
            'holidays': holidays,
        }

        return render(request, 'holidays/holidays.html', context)


def holiday_details(request, slug, destination=None, category=None):
    """ A view to show individual holiday details """
    holiday = get_object_or_404(Package.objects
                                .annotate(min_price=Min('price__price')), slug=slug)

    if category == 'offers':
        related_holidays = Package.objects.filter(offer=True).exclude(
            name=holiday.name).annotate(min_price=Min('price__price'))
        related_holidays = related_holidays.order_by('-rating')[:4]

    elif category:
        category = category.replace('-', ' ')
        related_holidays = Package.objects.exclude(name=holiday.name).annotate(
            lower_category=Lower('category__name'), min_price=Min('price__price'))
        related_holidays = related_holidays.filter(
            lower_category=category).order_by('-rating')[:4]

    else:
        destination = destination.replace('-', ' ')
        related_holidays = Package.objects.exclude(name=holiday.name).annotate(
            lower_region=Lower('country__region__name'), min_price=Min('price__price'))
        related_holidays = related_holidays.filter(
            lower_region=destination).order_by('-rating')[:4]

    context = {
        'holiday': holiday,
        'related_holidays': related_holidays,
        'category': category,
        'destination': destination,
    }
    return render(request, 'holidays/holiday_details.html', context)


@login_required
@superuser_required
def add_holiday(request):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = PackageForm(request.POST, request.FILES)

        if form.is_valid():
            holiday = form.save(commit=False)
            price_formset = PriceFormset(request.POST, instance=holiday)
            itinerary_formset = ItineraryFormset(
                request.POST, instance=holiday)

            if price_formset.is_valid() and itinerary_formset.is_valid():
                holiday.save()
                form.save_m2m()
                price_formset.save()
                itinerary_formset.save()
                messages.success(request, 'Successfully added holiday!')
                return redirect(redirect_url or reverse('destination_details', args=[holiday.country.region.slug, holiday.slug]))

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


@login_required
@superuser_required
def edit_holiday(request, package):
    holiday = get_object_or_404(Package, slug=package)
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = PackageForm(request.POST, request.FILES, instance=holiday)
        if form.is_valid():
            holiday = form.save(commit=False)
            price_formset = PriceFormset(request.POST, instance=holiday)
            itinerary_formset = ItineraryFormset(
                request.POST, instance=holiday)

            if price_formset.is_valid() and itinerary_formset.is_valid():
                holiday.save()
                form.save_m2m()
                price_formset.save()
                itinerary_formset.save()
                messages.success(request, 'Successfully updated holiday!')
                return redirect(redirect_url or reverse('destination_details', args=[holiday.country.region.slug, holiday.slug]))

        else:
            messages.error(
                request, 'Failed to update holiday. Please ensure the form is valid.')
    else:
        form = PackageForm(instance=holiday)
        price_formset = PriceFormset(instance=holiday)
        itinerary_formset = ItineraryFormset(instance=holiday)

    template = 'holidays/edit_holiday.html'
    context = {
        'form': form,
        'price_formset': price_formset,
        'itinerary_formset': itinerary_formset,
        'holiday': holiday,
    }

    return render(request, template, context)


@login_required
@superuser_required
def delete_holiday(request, package):
    holiday = get_object_or_404(Package, slug=package)
    holiday.delete()
    messages.success(request, 'Holiday deleted!')
    return redirect(reverse('destinations'))
