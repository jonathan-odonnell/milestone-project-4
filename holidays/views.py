from django.db.models.query import InstanceCheckMeta
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Package, Category, Region, Review
from booking.models import Booking
from profiles.models import UserProfile
from .forms import PackageForm, FeatureFormSet, ActivityFormSet, ItineraryFormSet, ReviewForm
from .utlis import superuser_required


def holidays(request, category=None, destination=None):
    """ A view to show all holidays for the category or destination, including sorting and search queries """
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

    if request.is_ajax():
        # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
        holidays_html = render_to_string(
            'holidays/includes/holiday_cards.html', {'holidays': holidays, 'category': category, 'destination': destination})
        return JsonResponse({'holidays': holidays_html})

    context = {
        'category': category,
        'destination': destination,
        'current_sorting': current_sorting,
        'categories': categories,
        'current_categories': current_categories,
        'countries': countries,
        'current_countries': current_countries,
        'holidays': holidays,
    }

    return render(request, 'holidays/holidays.html', context)


def holiday_details(request, slug, destination=None, category=None):
    """ A view to show individual holiday details """
    holiday = get_object_or_404(Package.objects, slug=slug)
    can_review = False

    if category:
        category = get_object_or_404(Category, slug=category)
        related_holidays = Package.objects.filter(category=category).exclude(
            name=holiday.name).order_by('?')[:4]

    elif destination:
        destination = get_object_or_404(Region, slug=destination)
        related_holidays = Package.objects.filter(region=destination).exclude(
            name=holiday.name).order_by('?')[:4]

    else:
        related_holidays = Package.objects.filter(offer=True).exclude(
            name=holiday.name).order_by('?')[:4]

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        bookings = Booking.objects.filter(
            user_profile=profile, package=holiday, paid=True)
        review = None

        if bookings:
            review = Review.objects.filter(
                package=holiday, full_name=profile.user.get_full_name()).first()

        if review:
            can_review = True

    context = {
        'holiday': holiday,
        'related_holidays': related_holidays,
        'category': category,
        'destination': destination,
        'can_review': can_review,
    }
    return render(request, 'holidays/holiday_details.html', context)


@login_required
def review(request, package):
    holiday = get_object_or_404(Package, slug=package)
    profile = UserProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(
        user_profile=profile, package=holiday, paid=True)
    review = None

    if bookings:
        review = Review.objects.filter(
            package=holiday, full_name=profile.user.get_full_name()).first()

    if review or not bookings:
        return HttpResponse(status=403)

    if request.POST:
        review_data = {
            'package': holiday,
            'full_name': profile.user.get_full_name(),
            'rating': request.POST['rating'],
            'title': request.POST['title'],
            'review': request.POST['review'],
        }
        form = ReviewForm(review_data)
        redirect_url = request.POST.get('redirect_url')

        if form.is_valid():
            form.save()
            return redirect(redirect_url or reverse('destination_details', args=[holiday.region.slug, holiday.slug]))

        messages.error(
            request, 'Failed to add review. Please ensure the form is valid.')

    else:
        form = ReviewForm()

    template = 'holidays/review.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
@superuser_required
def add_holiday(request):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = PackageForm(request.POST, request.FILES)
        feature_formset = FeatureFormSet(request.POST)
        activity_formset = ActivityFormSet(request.POST)
        itinerary_formset = ItineraryFormSet(request.POST)

        if form.is_valid():
            holiday = form.save()
            feature_formset = FeatureFormSet(request.POST, instance=holiday)
            activity_formset = ActivityFormSet(request.POST, instance=holiday)
            itinerary_formset = ItineraryFormSet(request.POST, instance=holiday)

            if feature_formset.is_valid():
                feature_formset.save()

                if activity_formset.is_valid():
                    activity_formset.save()

                    if itinerary_formset.is_valid():
                        itinerary_formset.save()

                        messages.success(
                            request, 'Successfully added holiday!')
                        return redirect(redirect_url or reverse('destination_details', args=[holiday.region.slug, holiday.slug]))

        messages.error(
            request, 'Failed to add holiday. Please ensure the form is valid.')

    else:
        form = PackageForm()
        feature_formset = FeatureFormSet()
        activity_formset = ActivityFormSet()
        itinerary_formset = ItineraryFormSet()

    template = 'holidays/add_holiday.html'
    context = {
        'form': form,
        'feature_formset': feature_formset,
        'activity_formset': activity_formset,
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
        feature_formset = FeatureFormSet(request.POST, instance=holiday)
        activity_formset = ActivityFormSet(request.POST, instance=holiday)
        itinerary_formset = ItineraryFormSet(request.POST, instance=holiday)

        if form.is_valid():
            form.save()

            if feature_formset.is_valid():
                feature_formset.save()

                if activity_formset.is_valid():
                    activity_formset.save()

                    if itinerary_formset.is_valid():
                        itinerary_formset.save()
                        messages.success(
                            request, 'Successfully updated holiday!')
                        return redirect(redirect_url or reverse('destination_details', args=[holiday.region.slug, holiday.slug]))

        else:
            messages.error(
                request, 'Failed to update holiday. Please ensure the form is valid.')
    else:
        form = PackageForm(instance=holiday)
        feature_formset = FeatureFormSet(instance=holiday)
        activity_formset = ActivityFormSet(instance=holiday)
        itinerary_formset = ItineraryFormSet(instance=holiday)

    template = 'holidays/edit_holiday.html'
    context = {
        'form': form,
        'feature_formset': feature_formset,
        'activity_formset': activity_formset,
        'itinerary_formset': itinerary_formset,
    }

    return render(request, template, context)


@login_required
@superuser_required
def delete_holiday(request, package):
    holiday = get_object_or_404(Package, slug=package)
    holiday.delete()
    messages.success(request, 'Holiday deleted!')
    return redirect(reverse('home'))
