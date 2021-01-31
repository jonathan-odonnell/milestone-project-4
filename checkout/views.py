from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from .forms import BookingForm
from .models import Booking, PackageBooking
from holidays.models import Package
from booking.contexts import booking_details
from django.conf import settings
import stripe
import datetime


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    booking = request.session.get('booking', {})

    if not booking:
            return HttpResponse(403)

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        booking_form = BookingForm(form_data)

        if booking_form.is_valid():
            current_booking = booking_form.save()
            try:
                holiday = Package.objects.get(id=booking['holiday_id'])
                package_booking = PackageBooking(
                            booking=current_booking,
                            package=holiday,
                            guests=int(booking['guests']),
                            departure_date=datetime.datetime.strptime(booking['departure_date'], "%d/%m/%Y").date(),
                            duration=holiday.duration,
                            total=booking_details(request)['subtotal']
                        )
                package_booking.save()
            
            except Package.DoesNotExist:
                    current_booking.delete()
                    return redirect(reverse('booking'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[current_booking.booking_number]))

    else:
        current_booking = booking_details(request)
        total = current_booking['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )
        
        booking_form = BookingForm()

    context = {
        'booking_form': booking_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'stripe_country': settings.STRIPE_COUNTRY,
        'stripe_currency': settings.STRIPE_CURRENCY,
        'stripe_total': stripe_total
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, booking_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    booking = get_object_or_404(Booking, booking_number=booking_number)

    if request.session.get('booking'):
        del request.session['booking']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
    }

    return render(request, template, context)
