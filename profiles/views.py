from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from checkout.models import Booking
from .forms import UserProfileForm


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user.email = request.POST['email_address']
            user_profile.save()

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
    }

    return render(request, template, context)

def bookings(request):
    """ Display the user's bookings. """
    profile = get_object_or_404(UserProfile, user=request.user)
    bookings = profile.bookings.all()

    template = 'profiles/bookings.html'
    context = {
        'bookings': bookings,
    }

    return render(request, template, context)

def booking_details(request, booking_number):
    booking = get_object_or_404(Booking, booking_number=booking_number)

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'from_booking': True,
    }

    return render(request, template, context)
