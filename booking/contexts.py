from django.conf import settings
from django.shortcuts import get_object_or_404
from holidays.models import Package, Price, Flight
import datetime
from decimal import Decimal


def booking_details(request):

    booking = request.session.get('booking', '')
    current_booking = {}
    current_date = datetime.datetime.now()
    holiday = None
    flights = []
    extras = 0
    coupon = None
    discount = 0
    subtotal = 0
    total = 0

    if booking:
        for key, value in booking.items():
            current_booking[key] = value

        holiday = get_object_or_404(Package, pk=current_booking['holiday_id'], price__start_date__lte=current_date, price__end_date__gte=current_date)
        current_booking['departure_date'] = datetime.datetime.strptime(current_booking['departure_date'], "%d/%m/%Y").date()
        current_booking['return_date'] = current_booking['departure_date'] + datetime.timedelta(days=int(holiday.duration))
        flights.append(Flight.objects.all().filter(outbound_flight__pk=current_booking['holiday_id'], origin=current_booking['departure_airport']))
        flights.append(Flight.objects.all().filter(inbound_flight__pk=current_booking['holiday_id'], destination=current_booking['departure_airport']))

        if booking.get('discount'):
            coupon = booking.get('coupon')
            discount = Decimal(booking.get('discount'))

        subtotal = Decimal(holiday.price_set.all()[0].price * booking['guests'])
        total = Decimal(subtotal + extras - discount)

    context = {
        'offer_amount': settings.OFFER_AMOUNT,
        'promo_code': settings.PROMO_CODE,
        'booking': current_booking,
        'holiday': holiday,
        'flights': flights,
        'coupon': coupon,
        'discount': discount,
        'subtotal': subtotal,
        'total': total
    }

    return context
