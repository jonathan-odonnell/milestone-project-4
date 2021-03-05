from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra
from checkout.models import Booking, BookingExtra, BookingPackage, BookingPassenger
from profiles.models import UserProfile
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
        Flight, packages__name=holiday.name, origin=request.POST.get('departure_airport'))
    return_flight = get_object_or_404(
        Flight, packages__name=holiday.name, destination=request.POST.get('departure_airport'))

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

    if booking.get('extras'):
        for key, value in booking['extras'].items():
            if value > guests:
                booking['extras'][key] = guests

    request.session['booking'] = booking
    booking_totals = booking_details(request)
    extras = booking_totals['extras_total']
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
def add_extra(request, extra_id):
    booking = request.session.get('booking')
    booking['extras'] = booking.get('extras', {})
    booking['extras'][extra_id] = booking['guests']
    request.session['booking'] = booking
    booking_totals = booking_details(request)
    extras = booking_totals['extras_total']
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
    extras = booking_totals['extras_total']
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
    extras = booking_totals['extras_total']
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
    coupon_name = request.POST.get('coupon')
    try:
        current_date = datetime.datetime.now()
        coupon = Coupon.objects.get(
            name__iexact=coupon_name, start_date__lte=current_date, end_date__gte=current_date)
        booking = request.session.get('booking')
        booking['coupon_id'] = coupon.pk
        booking['coupon'] = coupon_name
        request.session['booking'] = booking
        booking_totals = booking_details(request)
        discount = booking_totals['discount']
        subtotal = booking_totals['subtotal']
        total = booking_totals['total']

        response = {
            'success': True,
            'subtotal': subtotal,
            'total': total,
            'coupon': coupon_name,
            'discount': discount
        }

        return JsonResponse(response)

    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'coupon': coupon_name})


def passengers(request):
    if request.method == 'POST':
        booking = None
        current_booking = request.session.get('booking', {})
        passenger_range = range(current_booking['guests'])

        if current_booking.get('booking_number'):
            booking_number = current_booking.get('booking_number')
            booking = Booking.objects.get(booking_number=booking_number)
            booking.booking_package.delete()
            booking.booking_extras.all().delete()
            booking.booking_passengers.all().delete()
            booking.date = datetime.datetime.now()
            booking.save()

        else:
            booking = Booking()
            booking.save()

        try:
            holiday = Package.objects.get(id=current_booking['holiday_id'])
            outbound_flight = Flight.objects.get(
                pk=current_booking['outbound_flight'])
            return_flight = Flight.objects.get(
                pk=current_booking['return_flight'])
            booking_package = BookingPackage(
                booking=booking,
                package=holiday,
                guests=current_booking['guests'],
                departure_date=datetime.datetime.strptime(
                    current_booking['departure_date'], "%Y-%m-%d").date(),
                outbound_flight=outbound_flight,
                return_flight=return_flight,
                duration=holiday.duration,
            )
            booking_package.save()

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                booking.user_profile = profile
                booking.save()

            if current_booking.get('coupon'):
                booking.coupon = current_booking['coupon']
                booking.save()

            if current_booking.get('extras'):
                for extra_id, extra_quantity in current_booking['extras'].items():
                    try:
                        extra = Extra.objects.get(id=extra_id)
                        booking_extra = BookingExtra(
                            booking=booking,
                            extra=extra,
                            quantity=extra_quantity,
                        )
                        booking_extra.save()
                    
                    except Extra.DoesNotExist:
                        booking.delete()
                        return redirect(reverse('booking'))

            for passenger in passenger_range:
                booking_passenger = BookingPassenger(
                    booking=booking,
                    full_name=request.POST[f'name{passenger}'],
                    date_of_birth=datetime.datetime.strptime(
                    request.POST[f'dob{passenger}'], "%d/%m/%Y").date(),
                    passport_number=int(request.POST[f'passport{passenger}'])
                ) 
                booking_passenger.save()
            current_booking['booking_number'] = booking.booking_number
            request.session['booking'] = current_booking 

        except Package.DoesNotExist:
            booking.delete()
            return redirect(reverse('booking'))

        return redirect(reverse('checkout'))
    
    else:
        if request.session.get('booking'):
            profile = None

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)

            guests = request.session['booking']['guests']
            passenger_range = range(guests)
            context = {
                'passenger_range': passenger_range,
                'profile': profile,
            }
            return render(request, 'booking/passengers.html', context)

        else:
            return redirect(reverse('booking'))
