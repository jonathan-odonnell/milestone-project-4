from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Coupon, Booking
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra
import datetime
from decimal import Decimal


def booking_details(request):

    booking_number = request.session.get('booking_number', '')
    booking = None
    return_date = None
    extras_total = 0
    coupon = None
    discount = 0
    subtotal = 0
    total = 0

    if booking_number:
        booking = get_object_or_404(Booking, booking_number=booking_number)
        flight_departure = booking.booking_package.outbound_flight.departure_time
        flight_arrival = booking.booking_package.outbound_flight.departure_time
        flight_days = (flight_arrival - flight_departure).days
        return_date = booking.booking_package.departure_date + \
            datetime.timedelta(
                days=int(booking.booking_package.package.duration + flight_days + 1))

        if booking.booking_extras:
            for item in booking.booking_extras.all():
                total = item.total * item.quantity
                extras_total += total

        if booking.coupon:
            coupon = booking.coupon
            discount = booking.discount

        subtotal = booking.booking_package.total
        total = Decimal(subtotal + extras_total - discount)

    context = {
        'offer_amount': settings.OFFER_AMOUNT,
        'promo_code': settings.PROMO_CODE,
        'booking': booking,
        'return_date': return_date,
        'extras_total': extras_total,
        'coupon': coupon,
        'discount': discount,
        'subtotal': subtotal,
        'total': total
    }

    return context
