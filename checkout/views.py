from django.views.decorators.http import require_POST
from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .forms import BookingForm
from booking.models import Booking
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'booking_number': request.session['booking_number']
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    booking_number = request.session.get('booking_number', '')
    profile = None
    cards = None

    if not booking_number:
        return redirect(reverse('booking'))

    booking = Booking.objects.get(booking_number=booking_number)

    if request.method == 'POST':
        form_data = None
        save_info = 'save_info' in request.POST
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
        }

        booking_form = BookingForm(form_data, instance=booking)

        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.stripe_pid = pid
            booking.paid = True
            booking.save()

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                booking.user_profile = profile
                booking.save()

                if save_info:
                    profile_data = {
                        'phone_number': booking.phone_number,
                        'street_address1': booking.street_address1,
                        'street_address2': booking.street_address2,
                        'town_or_city': booking.town_or_city,
                        'county': booking.county,
                        'country': booking.country,
                        'postcode': booking.postcode,
                    }
                    user_profile_form = UserProfileForm(
                        profile_data, instance=profile)

                    if user_profile_form.is_valid():
                        user_profile_form.save()

            return redirect(reverse('checkout_success', args=[booking.booking_number]))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        total = booking.grand_total
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            booking_form = BookingForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.phone_number,
                'street_address1': profile.street_address1,
                'street_address2': profile.street_address2,
                'town_or_city': profile.town_or_city,
                'county': profile.county,
                'country': profile.country,
                'postcode': profile.postcode,
            })

            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                customer=profile.stripe_customer_id
            )

        else:
            booking_form = BookingForm()
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY
            )

    if request.user.is_authenticated:
        cards = stripe.PaymentMethod.list(
                customer=profile.stripe_customer_id,
                type="card",
                limit=3
            )

    context = {
        'booking_form': booking_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'stripe_country': settings.STRIPE_COUNTRY,
        'stripe_currency': settings.STRIPE_CURRENCY,
        'stripe_total': stripe_total,
        'cards': cards,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        'paypal_currency': settings.PAYPAL_CURRENCY,
        'google_api_key': settings.GOOGLE_PLACES_KEY,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, booking_number):
    """
    Handle successful checkouts
    """
    booking = get_object_or_404(Booking, booking_number=booking_number)
    time_zone = booking.outbound_flight.destination_time_zone.zone

    if request.session.get('booking_number'):
        del request.session['booking_number']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'time_zone': time_zone,
    }

    return render(request, template, context)


def paypal(request):
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    booking_number = request.session.get('booking_number', '')
    booking = Booking.objects.get(booking_number=booking_number)
    total = booking.grand_total
    currency = settings.PAYPAL_CURRENCY

    booking = Booking.objects.get(booking_number=booking_number)
    # From https://stackoverflow.com/questions/59630300/getting-bytes-when-using-axios
    form_data = json.loads(request.body)
    save_info = 'save_info' in form_data
    booking_form = BookingForm(form_data, instance=booking)

    if booking_form.is_valid:
        booking = booking_form.save()

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)

            if save_info:
                profile_data = {
                    'phone_number': booking.phone_number,
                    'street_address1': booking.street_address1,
                    'street_address2': booking.street_address2,
                    'town_or_city': booking.town_or_city,
                    'county': booking.county,
                    'country': booking.country,
                    'postcode': booking.postcode,
                }
                user_profile_form = UserProfileForm(
                    profile_data, instance=profile)

                if user_profile_form.is_valid():
                    profile.save()

    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)
    request = OrdersCreateRequest()
    request.headers['prefer'] = 'return=representation'
    request.request_body(
        {"intent": "CAPTURE",
         "application_context": {
             "brand_name": "Go Explore",
             "shipping_preference": "NO_SHIPPING"
         },
            "purchase_units":
            [{"reference_id": booking_number,
              "amount": {
                  "currency_code": currency,
                  "value": str(total),
              }}]})
    response = client.execute(request)
    response = response.result.__dict__['_dict']
    return JsonResponse(response)


def paypal_approve(request):
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    order_id = json.loads(request.body)['order_id']
    booking_number = request.session.get('booking_number', '')
    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)
    request = OrdersCaptureRequest(order_id)
    response = client.execute(request)
    response = response.result.__dict__['_dict']
    booking = Booking.objects.get(booking_number=booking_number)
    booking.paid = True
    booking.paypal_pid = response['id']
    booking.save()
    return JsonResponse(response)
