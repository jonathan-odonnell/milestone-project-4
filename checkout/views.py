from django.shortcuts import render, HttpResponse
from .forms import BookingForm
from booking.contexts import booking_details
from django.conf import settings
import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    booking = request.session.get('booking', {})

    if not booking:
        return HttpResponse(403)

    current_booking = booking_details(request)
    total = current_booking['total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )
    
    booking_form = BookingForm()

    context = {
        'booking_form': booking_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'stripe_country': settings.STRIPE_COUNTRY,
        'stripe_currency': settings.STRIPE_CURRENCY,
        'stripe_total': stripe_total
    }
    return render(request, 'checkout/checkout.html', context)
