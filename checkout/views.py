from django.views.decorators.http import require_POST
from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from .forms import BookingForm
from .models import Booking, BookingPackage
from holidays.models import Package
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from booking.contexts import booking_details
from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
import stripe
import datetime
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'booking_number': request.session['booking']['booking_number']
        })
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    profile = None

    if not current_booking:
        return HttpResponse(403)

    if request.method == 'POST':
        profile = None
        form_data = None
        save_info = 'save-info' in request.POST
        booking_number = request.session['booking']['booking_number']
        booking = Booking.objects.get(booking_number=booking_number)

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            if save_info:
                form_data = {
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'street_address1': request.POST['street_address1'],
                    'street_address2': request.POST['street_address2'],
                    'town_or_city': request.POST['town_or_city'],
                    'county': request.POST['county'],
                    'country': request.POST['country'],
                    'postcode': request.POST['postcode'],
                }

            else:
                form_data = {
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'street_address1': profile.street_address1,
                    'street_address2': profile.street_address2,
                    'town_or_city': profile.town_or_city,
                    'county': profile.county,
                    'country': profile.country,
                    'postcode': profile.postcode,
                }

        else:
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
            pid = request.POST.get('client_secret').split('_secret')[0]
            booking.stripe_pid = pid
            booking.paid = True
            booking.save()

            if request.user.is_authenticated:
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
        booking = booking_details(request)
        total = booking['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        cards = None

        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            cards = stripe.PaymentMethod.list(
                customer=profile.stripe_customer_id,
                type="card",
                limit=3
            )
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                customer=profile.stripe_customer_id
            )
        else:
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
        'stripe_total': stripe_total,
        'profile': profile,
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

    if request.session.get('booking'):
        del request.session['booking']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
    }

    return render(request, template, context)


def get_profile(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user)
        email = profile[0].user.email
        profile = list(profile.values())
        profile[0]['email'] = email
        profile = profile[0]
    else:
        profile = None
    return JsonResponse({'profile': profile})


def create_paypal_transaction(request):
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    booking = booking_details(request)
    total = booking['total']
    currency = settings.PAYPAL_CURRENCY
    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)
    create_transaction = OrdersCreateRequest()
    create_transaction.headers['prefer'] = 'return=representation'
    create_transaction.request_body(
        {"intent": "CAPTURE",
         "application_context": {
             "brand_name": "Travel Store",
             "shipping_preference": "NO_SHIPPING"
         },
            "purchase_units":
            [{"amount": {
             "currency_code": currency,
             "value": str(total),
             }}]})
    response = client.execute(create_transaction)
    data = response.result.__dict__['_dict']
    return JsonResponse(data)
