from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Coupon
from holidays.models import Package, Price, Flight
from extras.models import Extra
import datetime
from decimal import Decimal


def booking_details(request):

    booking = request.session.get('booking', '')
    current_booking = {}
    current_date = datetime.datetime.now()
    holiday = None
    flights = []
    extras = []
    extras_total = 0
    coupon = None
    discount = 0
    subtotal = 0
    total = 0

    if booking:
        for key, value in booking.items():
            current_booking[key] = value

        holiday = get_object_or_404(
            Package, pk=current_booking['holiday_id'], price__start_date__lte=current_date, price__end_date__gte=current_date)
        current_booking['departure_date'] = datetime.datetime.strptime(
            current_booking['departure_date'], "%Y-%m-%d").date()
        current_booking['return_date'] = datetime.datetime.strptime(
            current_booking['return_date'], "%Y-%m-%d").date()
        flights.append(get_object_or_404(
            Flight, pk=current_booking['outbound_flight']))
        flights.append(get_object_or_404(
            Flight, pk=current_booking['return_flight']))

        if booking.get('extras'):
            for extra_key, extra_value in booking['extras'].items():
                extra = get_object_or_404(Extra, pk=extra_key)
                extras_total += Decimal(extra.price * extra_value)
                extras.append({
                    'item_id': extra_key,
                    'quantity': extra_value,
                })
        if booking.get('coupon'):
            coupon = booking.get('coupon')
            discount = get_object_or_404(
                Coupon, name__iexact=booking['coupon'])
            discount = discount.amount

        subtotal = Decimal(holiday.price_set.all()[
                           0].price * booking['guests'])
        total = Decimal(subtotal + extras_total - discount)

    context = {
        'offer_amount': settings.OFFER_AMOUNT,
        'promo_code': settings.PROMO_CODE,
        'booking': current_booking,
        'holiday': holiday,
        'flights': flights,
        'extras_total': extras_total,
        'extras': extras,
        'coupon': coupon,
        'discount': discount,
        'subtotal': subtotal,
        'total': total
    }

    return context
