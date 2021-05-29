from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.forms import inlineformset_factory
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra
from .models import Booking, BookingPassenger, BookingExtra, Coupon
from profiles.models import UserProfile
from .forms import PassengerForm
from .contexts import booking_details
from pytz import timezone
import datetime


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
                packages__name=holiday.name, origin=request.POST['departure_airport'])
            return_flight = Flight.objects.get(
                packages__name=holiday.name, destination=request.POST['departure_airport'])
            time_zone = outbound_flight.destination_time_zone
            flight_arrival = outbound_flight.departure_time.astimezone(
                time_zone)
            flight_days = (flight_arrival -
                           outbound_flight.departure_time).days
            departure_date = datetime.datetime.strptime(
                request.POST['departure_date'], "%d/%m/%Y").date()
            return_date = departure_date + \
                datetime.timedelta(
                    days=int(holiday.duration + flight_days + 1))

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
                request, 'Unable to find flights. Please select another date and try again.')
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
    booking = Booking.objects.get(booking_number=booking_number)
    booking_extras = booking.booking_extras.get(extra=extra_id)
    booking_extras.quantity = quantity
    booking_extras.save()

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
    booking = Booking.objects.get(booking_number=booking_number)
    booking.booking_extras.get(extra=extra_id).delete()

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
        current_date = datetime.datetime.now()
        coupon = Coupon.objects.get(
            name__iexact=coupon_name, start_date__lte=current_date, end_date__gte=current_date)
        booking.coupon = coupon.name
        booking.save()

        # https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros

        discount = f'{float(booking.discount):g}'
        subtotal = f'{float(booking.subtotal):g}'
        total = f'{float(booking.grand_total):g}'

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

        formset = inlineformset_factory(
            Booking,
            BookingPassenger,
            form=PassengerForm,
            extra=booking.guests
        )

        formset = formset(
            request.POST, 
            instance=booking
        )

        if formset.is_valid():
            formset.save()
            return redirect(reverse('checkout'))

        else:
            messages.error(
                request, 'Unable to add passenger details. Please ensure the form is valid.')

    else:

        if request.user.is_authenticated and not booking.booking_passengers.all():
            profile = UserProfile.objects.get(user=request.user)
            formset = inlineformset_factory(
                Booking,
                BookingPassenger,
                form=PassengerForm,
                extra=booking.guests,
            )
            formset = formset(
                initial=[
                    {'full_name': profile.user.get_full_name()}
                ],
            )

        elif booking.booking_passengers.all():
            formset = inlineformset_factory(
                Booking,
                BookingPassenger,
                form=PassengerForm,
                extra=0,
            )
            formset = formset(
                instance=booking
            )

        else:  
            formset = inlineformset_factory(
                Booking,
                BookingPassenger,
                form=PassengerForm,
                extra=booking.guests
            )

    context = {
        'formset': formset,
    }

    return render(request, 'booking/passengers.html', context)
