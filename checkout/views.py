from django.shortcuts import render
from .forms import BookingForm

def checkout(request):
    booking = request.session.get('booking', {})
    booking_form = BookingForm()
    context = {
        'booking_form': booking_form,
        'stripe_public_key': "",
        'client_secret': ""
    }
    return render(request, 'checkout/checkout.html', context)
