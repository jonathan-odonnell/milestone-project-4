from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra
from .models import Booking, BookingExtra, Coupon
from profiles.models import UserProfile
from .forms import PassengersFormSet
from datetime import datetime, date, timedelta


def booking(request):
    return render(request, 'booking/booking.html')


@require_POST
def add_booking(request, holiday_id):
    if request.method == 'POST':
        booking = None
        booking_number = request.session.get('booking_number', '')
        holiday = Package.objects.get(pk=holiday_id)

        try:
            outbound_flight = Flight.objects.get(
                packages__name=holiday.name,
                origin=request.POST['departure_airport'])
            return_flight = Flight.objects.get(
                packages__name=holiday.name,
                destination=request.POST['departure_airport'])
            departure_date = datetime.strptime(
                request.POST['departure_date'], "%d/%m/%Y").date()
            outbound_flight_departure = outbound_flight.departure_time \
                .astimezone(outbound_flight.origin_time_zone)
            outbound_flight_arrival = outbound_flight.arrival_time \
                .astimezone(outbound_flight.destination_time_zone)
            flight_days = (outbound_flight_arrival -
                           outbound_flight_departure).days
            return_date = departure_date + timedelta(
                days=int(holiday.duration + flight_days))

            if booking_number:
                booking = Booking.objects.filter(
                    booking_number=booking_number).delete()

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                booking = Booking(
                    user_profile=profile,
                    package=holiday,
                    guests=int(request.POST['guests']),
                    departure_date=departure_date,
                    return_date=return_date,
                    outbound_flight=outbound_flight,
                    return_flight=return_flight
                )
                booking.save()

            else:
                booking = Booking(
                    package=holiday,
                    guests=int(request.POST['guests']),
                    departure_date=departure_date,
                    return_date=return_date,
                    outbound_flight=outbound_flight,
                    return_flight=return_flight
                )
                booking.save()

            request.session['booking_number'] = booking.booking_number

        except Flight.DoesNotExist:
            messages.error(
                request,
                'Unable to find flights. '
                'Please select another date and try again.')
            return(redirect(request.META.get('HTTP_REFERER') or reverse('home')))

    return redirect(reverse('booking'))


@require_POST
def update_guests(request):
    booking_number = request.session.get('booking_number')
    booking = Booking.objects.get(booking_number=booking_number)
    guests = int(request.POST.get('guests'))
    booking.guests = guests
    booking.save()

    if booking.booking_extras.all():
        for extra in booking.booking_extras.all():
            if extra.quantity > guests:
                extra.quantity = guests
                extra.save()

    # https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros

    extras = f'{float(booking.extras_total):g}'
    subtotal = f'{float(booking.subtotal):g}'
    total = f'{float(booking.grand_total):g}'

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
    extra_quantity = int(request.POST['quantity'])
    booking_extra = BookingExtra(
        booking=booking,
        extra=extra,
        quantity=extra_quantity,
    )
    booking_extra.save()

    # https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros

    extras = f'{float(booking.extras_total):g}'
    subtotal = f'{float(booking.subtotal):g}'
    total = f'{float(booking.grand_total):g}'

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
    booking = Booking.objects.prefetch_related('booking_extras').get(
        booking_number=booking_number, booking_extras__extra=extra_id)
    booking.booking_extras.all()[0].quantity = quantity
    booking.booking_extras.all()[0].save()

    # https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros

    extras = f'{float(booking.extras_total):g}'
    subtotal = f'{float(booking.subtotal):g}'
    total = f'{float(booking.grand_total):g}'

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
    booking = Booking.objects.prefetch_related('booking_extras').get(
        booking_number=booking_number, booking_extras__extra=extra_id)
    booking.booking_extras.first().delete()

    # https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros

    extras = f'{float(booking.extras_total):g}'
    subtotal = f'{float(booking.subtotal):g}'
    total = f'{float(booking.grand_total):g}'

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
        current_date = date.today()
        coupon = Coupon.objects.get(
            name__iexact=coupon_name,
            start_date__lte=current_date,
            end_date__gte=current_date)
        booking.coupon = coupon.name
        booking.save()

        # https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros

        subtotal = f'{float(booking.subtotal):g}'
        total = f'{float(booking.grand_total):g}'
        discount = f'{float(booking.discount):g}'
        coupon_name = coupon.name

        response = {
            'subtotal': subtotal,
            'total': total,
            'coupon': coupon_name,
            'discount': discount
        }

        return JsonResponse(response)

    except Coupon.DoesNotExist:
        return HttpResponse(status=500)


def passengers(request):
    booking_number = request.session.get('booking_number', '')
    profile = None

    if not booking_number:
        return redirect(reverse('booking'))

    booking = get_object_or_404(Booking, booking_number=booking_number)

    if request.method == 'POST':

        formset = PassengersFormSet(
            request.POST,
            instance=booking,
            min_num=booking.guests,
        )

        if formset.is_valid():
            formset.save()
            return redirect(reverse('checkout'))

        else:
            messages.error(
                request,
                'Unable to add passenger details. '
                'Please ensure the form is valid.')

    else:
        if (request.user.is_authenticated
                and not booking.booking_passengers.all()):
            profile = UserProfile.objects.get(user=request.user)
            formset = PassengersFormSet(
                initial=[
                    {'full_name': profile.user.get_full_name()}
                ],
                min_num=booking.guests,
            )

        elif booking.booking_passengers.all():
            formset = PassengersFormSet(
                instance=booking,
                min_num=booking.guests,
            )

        else:
            formset = PassengersFormSet(
                min_num=booking.guests,
            )
    context = {
        'formset': formset,
    }

    return render(request, 'booking/passengers.html', context)
