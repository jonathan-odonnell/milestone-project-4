from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Booking


def booking_details(request):

    booking_number = request.session.get('booking_number', '')
    booking = None
    outbound_flight_duration = None
    return_flight_duration = None
    time_zone = None
    selected_extras = []

    if booking_number:
        booking = get_object_or_404(Booking, booking_number=booking_number)
        outbound_flight_duration = booking.booking_package.outbound_flight.arrival_time - booking.booking_package.outbound_flight.departure_time
        return_flight_duration = booking.booking_package.return_flight.arrival_time - booking.booking_package.return_flight.departure_time
        time_zone = booking.booking_package.outbound_flight.destination_time_zone.zone
        if booking.booking_extras.all():
            for extra in booking.booking_extras.all():
                selected_extras.append(extra.extra.id)

        

    context = {
        'offer_amount': settings.OFFER_AMOUNT,
        'promo_code': settings.PROMO_CODE,
        'booking': booking,
        'selected_extras': selected_extras,
        'outbound_flight_duration': outbound_flight_duration,
        'return_flight_duration': return_flight_duration,
        'time_zone': time_zone,
    }

    return context
