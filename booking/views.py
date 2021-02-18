from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from holidays.models import Package, Flight
from extras.models import Extra
from .models import Coupon
from .contexts import booking_details
import datetime
from decimal import Decimal


def booking(request):
    return render(request, 'booking/booking.html')


@require_POST
def add_booking(request, holiday_id):
    date = datetime.datetime.now()
    holiday = get_object_or_404(
        Package, pk=holiday_id, price__start_date__lte=date, price__end_date__gte=date)
    departure_date = datetime.datetime.strptime(
        request.POST.get('departure_date'), "%d/%m/%Y").date()
    return_date = departure_date + \
        datetime.timedelta(days=int(holiday.duration))
    outbound_flight = get_object_or_404(
        Flight, outbound_flight__name=holiday.name, origin=request.POST.get('departure_airport'))
    return_flight = get_object_or_404(
        Flight, inbound_flight__name=holiday.name, destination=request.POST.get('departure_airport'))

    guests = int(request.POST.get('guests'))
    booking = request.session.get('booking', {})
    booking['holiday_id'] = holiday_id
    booking['price'] = str(holiday.price_set.all()[0].price)
    booking['guests'] = guests
    booking['departure_airport'] = request.POST.get('departure_airport')
    booking['departure_date'] = str(departure_date)
    booking['return_date'] = str(return_date)
    booking['outbound_flight'] = outbound_flight.pk
    booking['return_flight'] = return_flight.pk

    request.session['booking'] = booking

    return redirect(reverse('booking'))


@require_POST
def update_guests(request):
    booking = request.session.get('booking')
    guests = int(request.POST.get('guests'))
    booking['guests'] = guests
    request.session['booking'] = booking
    subtotal = booking_details(request)['subtotal']
    total = booking_details(request)['total']

    response = {
        'success': True,
        'subtotal': subtotal,
        'total': total,
    }

    return JsonResponse(response)


@require_POST
def add_extra(request, extra_id):
    booking = request.session.get('booking')
    booking['extras'] = booking.get('extras', {})
    booking['extras'][extra_id] = booking['guests']
    request.session['booking'] = booking
    booking_totals = booking_details(request)
    extras = booking_totals['extras']
    subtotal = booking_totals['subtotal']
    total = booking_totals['total']
    
    response = {
        'success': True,
        'extras': extras,
        'subtotal': subtotal,
        'total': total,
    }

    return JsonResponse(response)


@require_POST
def update_extra(request, extra_id):
    booking = request.session.get('booking')
    quantity = int(request.POST['quantity'])
    booking['extras'][extra_id] = quantity
    request.session['booking'] = booking
    booking_totals = booking_details(request)
    extras = booking_totals['extras']
    subtotal = booking_totals['subtotal']
    total = booking_totals['total']
    
    response = {
        'success': True,
        'extras': extras,
        'subtotal': subtotal,
        'total': total,
    }
    return JsonResponse(response)


@require_POST
def remove_extra(request, extra_id):
    booking = request.session.get('booking')
    del booking['extras'][extra_id]
    request.session['booking'] = booking
    booking_totals = booking_details(request)
    extras = booking_totals['extras']
    subtotal = booking_totals['subtotal']
    total = booking_totals['total']
    
    response = {
        'success': True,
        'extras': extras,
        'subtotal': subtotal,
        'total': total,
    }

    return JsonResponse(response)


@require_POST
def add_coupon(request):
    try:
        current_date = datetime.datetime.now()
        coupon_name = request.POST.get('coupon')
        coupon = get_object_or_404(
            Coupon, name__iexact=coupon_name, start_date__lte=current_date, end_date__gte=current_date)
        booking = request.session.get('booking')
        booking['coupon_id'] = coupon.pk
        booking['coupon'] = coupon_name
        request.session['booking'] = booking
        discount = booking_details(request)['discount']
        subtotal = booking_details(request)['subtotal']
        total = booking_details(request)['total']

        response = {
            'success': True,
            'subtotal': subtotal,
            'total': total,
            'coupon': coupon_name,
            'discount': discount
        }

        return JsonResponse(response)

    except ObjectDoesNotExist:
        return JsonResponse({'success': False})
