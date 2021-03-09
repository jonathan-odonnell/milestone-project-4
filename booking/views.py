from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra
from .models import Booking, BookingExtra, BookingPackage, BookingPassenger, Coupon
from profiles.models import UserProfile
from .contexts import booking_details
import datetime
from decimal import Decimal


def booking(request):
    return render(request, 'booking/booking.html')


@require_POST
def add_booking(request, holiday_id):
    if request.method == 'POST':
        booking = None
        booking_number = request.session.get('booking_number', '')

        try:
            holiday = get_object_or_404(Package, pk=holiday_id)
            outbound_flight = Flight.objects.get(
                packages__name=holiday.name, origin=request.POST['departure_airport'])
            return_flight = Flight.objects.get(
                packages__name=holiday.name, destination=request.POST['departure_airport'])

            if booking_number:
                booking = Booking.objects.get(booking_number=booking_number)
                booking.booking_package.delete()
                booking.booking_extras.all().delete()
                booking.booking_passengers.all().delete()
                booking.date = datetime.datetime.now()
                booking.save()

            else:
                if request.user.is_authenticated:
                    try:
                        profile = UserProfile.objects.get(user=request.user)
                        booking = Booking(user_profile=profile)
                        booking.save()

                    except UserProfile.DoesNotExist:
                        booking = Booking()
                        booking.save()

                else:
                    booking = Booking(user_profile=profile)
                    booking.save()

                request.session['booking_number'] = booking.booking_number

            booking_package = BookingPackage(
                booking=booking,
                package=holiday,
                guests=int(request.POST['guests']),
                departure_date=datetime.datetime.strptime(
                    request.POST['departure_date'], "%d/%m/%Y").date(),
                outbound_flight=outbound_flight,
                return_flight=return_flight,
                duration=holiday.duration,
            )
            booking_package.save()

        except Flight.DoesNotExist:
            messages.error(
                request, 'Unable to find flights. Please select another date and try again.')
            return(redirect(request.META.get('HTTP_REFERER') or reverse('home')))

    return redirect(reverse('booking'))
3

@require_POST
def update_guests(request):
    booking_number = request.session.get('booking_number')
    booking = Booking.objects.get(booking_number=booking_number)
    guests = int(request.POST.get('guests'))
    booking.booking_package.guests = guests
    booking.booking_package.save()

    if booking.booking_extras.all():
        for extra in booking.booking_extras.all():
            if extra.quantity > guests:
                extra.update(quantity=guests)

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
    booking_number = request.session.get('booking_number')
    booking = Booking.objects.get(booking_number=booking_number)
    extra = Extra.objects.get(id=extra_id)
    extra_quantity = 1
    booking_extra = BookingExtra(
        booking=booking,
        extra=extra,
        quantity=extra_quantity,
    )
    booking_extra.save()
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
    booking_number = request.session.get('booking_number')
    quantity = int(request.POST['quantity'])
    BookingExtra.objects.filter(
        booking__booking_number=booking_number, extra__pk=extra_id).update(quantity=quantity)
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
    booking_number = request.session.get('booking_number')
    BookingExtra.objects.filter(
        booking__booking_number=booking_number, extra__pk=extra_id).delete()
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
    booking_number = request.session.get('booking_number')
    booking = get_object_or_404(Booking, booking_number=booking_number)
    try:
        current_date = datetime.datetime.now()
        coupon = Coupon.objects.get(
            name__iexact=coupon_name, start_date__lte=current_date, end_date__gte=current_date)
        booking.coupon = coupon.name
        booking.save()
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
    booking_number = request.session.get('booking_number', '')
    if request.method == 'POST':
        booking = Booking.objects.get(booking_number=booking_number)
        passenger_range = range(booking.booking_package.guests)

        if booking_number:
            for passenger in passenger_range:
                booking_passenger = BookingPassenger(
                    booking=booking,
                    full_name=request.POST[f'name{passenger}'],
                    date_of_birth=datetime.datetime.strptime(
                        request.POST[f'dob{passenger}'], "%d/%m/%Y").date(),
                    passport_number=int(request.POST[f'passport{passenger}'])
                )
                booking_passenger.save()

        else:
            return redirect(reverse('booking'))

        return redirect(reverse('checkout'))

    else:
        profile = None
        if not booking_number:
            return redirect(reverse('booking'))

        else:
            try:
                booking = Booking.objects.get(booking_number=booking_number)
                passenger_range = range(booking.booking_package.guests)

                if request.user.is_authenticated:
                    profile = UserProfile.objects.get(user=request.user)

            except Booking.DoesNotExist:
                return redirect(reverse('booking'))

            context = {
                'passenger_range': passenger_range,
                'profile': profile,
            }

            return render(request, 'booking/passengers.html', context)
