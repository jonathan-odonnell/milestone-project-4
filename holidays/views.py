from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import Package, Category, Region, Review
from booking.models import Booking
from profiles.models import UserProfile
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PackageForm, FeatureFormset, ActivityFormset, ItineraryFormset, ReviewForm
from .utlis import superuser_required, get_holidays


def holidays(request, category=None, destination=None):
    """ A view to show all holidays for the category or destination, including sorting and search queries """
    
    holidays_data = get_holidays(request, category, destination)
    holidays = holidays_data['holidays']
    category = holidays_data['category']
    destination = holidays_data['destination']
    current_sorting = holidays_data['current_sorting']
    categories = holidays_data['categories']
    current_categories = holidays_data['current_categories']
    countries = holidays_data['countries']
    current_countries = holidays_data['current_countries']

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


def filter_holidays(request, destination=None, category=None):
    holidays_data = get_holidays(request, category, destination)
    holidays = holidays_data['holidays']
    category = holidays_data['category']
    destination = holidays_data['destination']
    # https://stackoverflow.com/questions/50879653/django-render-template-in-template-using-ajax
    html = render_to_string(
        'holidays/includes/holiday_cards.html', {'holidays': holidays, 'category': category, 'destination': destination})
    return JsonResponse({'holidays': html})


def holiday_details(request, slug, destination=None, category=None):
    """ A view to show individual holiday details """
    holiday = get_object_or_404(Package.objects, slug=slug)
    not_reviewed = False

    if category:
        category = get_object_or_404(Category, slug=category)
        holidays = Package.objects.exclude(name=holiday.name).filter(category=category).order_by('?')[:4]
    
    if destination:
        destination = get_object_or_404(Region, slug=destination)
        holidays = Package.objects.exclude(name=holiday.name).filter(region=destination).order_by('?')[:4]

    else:
        holidays = Package.objects.filter(offer=True).exclude(name=holiday.name).order_by('?')[:4]
    
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        bookings = Booking.objects.filter(user_profile=profile, package=holiday, paid=True)
        
        if bookings:
            try:
                Review.objects.get(package=holiday, full_name=profile.user.get_full_name())

            except Review.DoesNotExist:
                not_reviewed = True

    context = {
        'holiday': holiday,
        'holidays': holidays,
        'category': category,
        'destination': destination,
        'not_reviewed': not_reviewed,
    }
    return render(request, 'holidays/holiday_details.html', context)

@login_required
def review(request, package):
    holiday = get_object_or_404(Package, slug=package)
    profile = UserProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(user_profile=profile, booking_package__package=holiday)
    
    if not bookings:
        return HttpResponse(status=403)

    if bookings:
        try:
            Review.objects.get(package=holiday, name=profile.user.get_full_name())
            return HttpResponse(status=403)

        except Review.DoesNotExist:
            pass

    if request.POST:
        review_data = {
            'full_name': profile.user.get_full_name(),
            'rating': request.POST['rating'],
            'title': request.POST['title'],
            'review': request.POST['review'],
        }
        form = ReviewForm(review_data, instance=holiday)
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

        if form.is_valid():
            holiday = form.save()
            feature_formset = FeatureFormset(
                request.POST, instance=holiday
            )
            activity_formset = ActivityFormset(
                request.POST, instance=holiday
            )
            itinerary_formset = ItineraryFormset(
                request.POST, instance=holiday
            )

            if feature_formset.is_valid():
                feature_formset.save()
            
                if activity_formset.is_valid():
                    activity_formset.save()

                    if itinerary_formset.is_valid():
                        itinerary_formset.save()
                        messages.success(request, 'Successfully added holiday!')
                        return redirect(redirect_url or reverse('destination_details', args=[holiday.region.slug, holiday.slug]))

        messages.error(
            request, 'Failed to add holiday. Please ensure the form is valid.')

    else:
        form = PackageForm()
        feature_formset = FeatureFormset()
        activity_formset = ActivityFormset()
        itinerary_formset = ItineraryFormset()

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
        feature_formset = FeatureFormset(request.POST, instance=holiday)
        activity_formset = ActivityFormset(request.POST, instance=holiday)
        itinerary_formset = ItineraryFormset(request.POST, instance=holiday)
        
        if form.is_valid():
            form.save()
            
            if feature_formset.is_valid():
                feature_formset.save()

                if activity_formset.is_valid():
                    activity_formset.save()

                    if itinerary_formset.is_valid():
                        itinerary_formset.save()
                        messages.success(request, 'Successfully updated holiday!')
                        return redirect(redirect_url or reverse('destination_details', args=[holiday.region.slug, holiday.slug]))

        else:
            messages.error(
                request, 'Failed to update holiday. Please ensure the form is valid.')
    else:
        form = PackageForm(instance=holiday)
        feature_formset = FeatureFormset(instance=holiday)
        activity_formset = ActivityFormset(instance=holiday)
        itinerary_formset = ItineraryFormset(instance=holiday)

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
