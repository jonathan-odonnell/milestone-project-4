from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Coupon, Booking


def booking_details(request):

    booking_number = request.session.get('booking_number', '')
    booking = None
    selected_extras = []

    if booking_number:
        booking = get_object_or_404(Booking, booking_number=booking_number)

        if booking.booking_extras.all():
            for extra in booking.booking_extras.all():
                selected_extras.append(extra.extra.id)

    context = {
        'offer_amount': settings.OFFER_AMOUNT,
        'promo_code': settings.PROMO_CODE,
        'booking': booking,
        'selected_extras': selected_extras,
    }

    return context
