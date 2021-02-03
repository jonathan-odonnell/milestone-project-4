from django.views.decorators.http import require_POST
from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from .forms import BookingForm
from .models import Booking, PackageBooking
from holidays.models import Package
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from booking.contexts import booking_details
from django.conf import settings
import stripe
import datetime
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'booking': json.dumps(request.session.get('booking', {})),
            'save_info': request.POST.get('save_info'),
            'save_card': request.POST.get('save_card'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    current_booking = request.session.get('booking', {})
    profile = None

    if not current_booking:
        return HttpResponse(403)

    if request.method == 'POST':
        profile = None
        form_data = None
        save_info = 'save-info' in request.POST
        save_card = 'save-card' in request.POST

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

        booking_form = BookingForm(form_data)

        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            booking.stripe_pid = pid
            booking.save()

            try:
                holiday = Package.objects.get(id=current_booking['holiday_id'])
                package_booking = PackageBooking(
                    booking=booking,
                    package=holiday,
                    guests=int(current_booking['guests']),
                    departure_date=datetime.datetime.strptime(
                        current_booking['departure_date'], "%d/%m/%Y").date(),
                    duration=holiday.duration,
                    total=booking_details(request)['subtotal']
                )
                package_booking.save()

            except Package.DoesNotExist:
                booking.delete()
                return redirect(reverse('booking'))

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

                if save_card and not profile.stripe_customer_id:

                    customer = stripe.Customer.create(
                        name=profile.user.get_full_name(),
                        email=profile.user.email,
                        address={
                            'line1': profile.street_address1,
                            'line2': profile.street_address2,
                            'city': profile.town_or_city,
                            'state': profile.county,
                            'country': profile.country,
                            'postal_code': profile.postcode,
                        }
                    )

                    profile.update(stripe_customer_id=customer.id)

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
