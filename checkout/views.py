from django.views.decorators.http import require_POST
from django.shortcuts import (
    render, HttpResponse, redirect, reverse, get_object_or_404)
from django.contrib import messages
from django.conf import settings
from booking.models import Booking
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import BookingForm
from .webhook_handler import WH_Handler
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    A view to amend the payment intent metadata and add the save_info,
    username and booking_number values.
    """
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
    """
    A view to set up the payment intent, display the checkout page and process
    the booking form once the payment has been approved.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    booking_number = request.session.get('booking_number', '')
    profile = None
    cards = None

    """
    Checks that there is a valid booking number in the browser's session
    variable and passenger details have been added to the booking.
    """
    if not booking_number:
        return redirect(reverse('booking'))

    else:
        booking = Booking.objects.get(booking_number=booking_number)

    if not booking.booking_passengers.all():
        return redirect(reverse('passengers'))

    if request.method == 'POST':
        save_info = 'save_info' in request.POST
        stripe_pid = request.POST['client_secret'].split('_secret')[0]
        paypal_pid = request.POST['paypal_pid']
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Saves the booking form if it is valid
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

            # Adds the relevant payment id to the booking and sets paid to true
            if paypal_pid:
                booking.paypal_pid = paypal_pid
                booking.paid = True

            else:
                booking.stripe_pid = stripe_pid
                booking.paid = True

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                booking.user_profile = profile
                booking.save()

                """
                Saves the user's details to their profile if the
                save info checkbox box was checked in the form
                """
                if save_info:
                    profile_data = {
                        'email_address': profile.user.email,
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

            else:
                booking.save()

            # Sends the confirmation email if the payment method was paypal
            if paypal_pid:
                handler = WH_Handler(request)
                handler.send_confirmation_email(booking)

            return redirect(reverse('checkout_success',
                                    args=[booking.booking_number]))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        total = booking.grand_total
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        if request.user.is_authenticated:
            """
            Creates a booking form filled in with the user's profile data
            and a new payment intent with their customer id attached. Code
            is from https://stripe.com/docs/payments/save-during-payment
            """
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
            """
            Creates an empty booking form and a new payment intent
            with no customer id attached
            """
            booking_form = BookingForm()
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY
            )

    """
    Gets up to 3 of the customer's latest saved cards if they are logged in.
    Code is from https://stripe.com/docs/api/cards/list
    """
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
    A view to handle successful checkouts and display the
    checkout success page.
    """
    booking = get_object_or_404(Booking, booking_number=booking_number)

    if request.session.get('booking_number'):
        del request.session['booking_number']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
    }

    return render(request, template, context)


def paypal(request):
    """
    A view to set up a paypal transaction. Code is from
    https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/
    and
    https://developer.paypal.com/docs/checkout/reference/server-integration/set-up-transaction/
    """
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    booking_number = request.session.get('booking_number', '')
    booking = Booking.objects.get(booking_number=booking_number)
    total = booking.grand_total
    currency = settings.PAYPAL_CURRENCY
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
    return response


def paypal_approve(request):
    """
    A view to capture the paypal transaction funds. Code is from
    https://stackoverflow.com/questions/59630300/getting-bytes-when-using-axios
    and
    https://developer.paypal.com/docs/checkout/reference/server-integration/capture-transaction/
    """
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    order_id = json.loads(request.body)['order_id']
    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)
    request = OrdersCaptureRequest(order_id)
    response = client.execute(request)
    return response
