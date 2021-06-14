from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from booking.models import Booking
from .forms import UserProfileForm
from django.conf import settings
import stripe


@login_required
def profile(request):
    """
    A view to display the profile page and
    update the user's profile in the database.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    api_key = settings.GOOGLE_PLACES_KEY

    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.user.email = request.POST['email_address']
            profile.user.save()

    else:
        form = UserProfileForm(
            initial={'email_address': profile.user.email,
                     'phone_number': profile.phone_number,
                     'street_address1': profile.street_address1,
                     'street_address2': profile.street_address2,
                     'town_or_city': profile.town_or_city,
                     'county': profile.county,
                     'country': profile.country,
                     'postcode': profile.postcode,
                     })

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'api_key': api_key,
    }

    return render(request, template, context)


@login_required
def bookings(request):
    """ A view to show the bookings page."""
    profile = get_object_or_404(UserProfile, user=request.user)
    bookings = profile.bookings.filter(paid=True)

    template = 'profiles/bookings.html'
    context = {
        'bookings': bookings,
    }

    return render(request, template, context)


@login_required
def booking_details(request, booking_number):
    """A view to show the booking details page."""
    booking = get_object_or_404(Booking, booking_number=booking_number)

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'from_booking': True,
    }

    return render(request, template, context)
