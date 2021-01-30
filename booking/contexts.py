from django.conf import settings
from django.shortcuts import get_object_or_404
from holidays.models import Package, Price, Flight
import datetime
from decimal import Decimal


def booking_details(request):

    booking = request.session.get('booking')
    date = datetime.datetime.now()
    holiday = None
    flights = []
    extras = 0
    coupon = None
    discount = 0
    subtotal = 0
    total = 0

    if booking:
        holiday = get_object_or_404(Package, pk=booking['holiday_id'], price__start_date__lte=date, price__end_date__gte=date)
        booking['departure_date'] = datetime.datetime.strptime(booking['departure_date'], "%Y-%m-%d").date()
        booking['return_date'] = booking['departure_date'] + datetime.timedelta(days=int(holiday.duration))
        flights.append(Flight.objects.all().filter(outbound_flight__pk=booking['holiday_id'], origin=booking['departure_airport']))
        flights.append(Flight.objects.all().filter(inbound_flight__pk=booking['holiday_id'], destination=booking['departure_airport']))

        if booking.get('discount'):
            coupon = booking.get('coupon')
            discount = Decimal(booking.get('discount'))

        subtotal = Decimal(holiday.price_set.all()[0].price * booking['guests'])
        total = Decimal(subtotal + extras - discount)

    context = {
        'booking': booking,
        'holiday': holiday,
        'flights': flights,
        'coupon': coupon,
        'discount': discount,
        'subtotal': subtotal,
        'total': total
    }

    return context
