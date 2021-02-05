from django.http import HttpResponse
from .models import Booking, PackageBooking
from holidays.models import Package
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from booking.contexts import booking_details
import time
import datetime


class StripeWH_Handler:
    "Handles stripe webhooks"

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handles a generic/unexpected/unknown webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handles the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        current_booking = intent.metadata.booking
        save_info = intent.metadata.save_info
        save_card = intent.metadata.save_card
        username = intent.metadata.username
        profile = None

        billing_details = intent.charges.data[0].billing_details
        total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        booking_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                booking = Booking.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    town_or_city__iexact=billing_details.address.city,
                    county__iexact=billing_details.address.state,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    total=total,
                    stripe_pid=pid,
                )
                booking_exists = True
                break

            except Booking.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if booking_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)

        else:
            booking = None
            try:
                booking = Booking.objects.create(
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    town_or_city=billing_details.address.city,
                    county=billing_details.address.state,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    stripe_pid=pid,
                )
                holiday = Package.objects.get(id=current_booking['holiday_id'])
                package_booking = PackageBooking(
                    booking=booking,
                    package=holiday,
                    guests=int(current_booking['guests']),
                    departure_date=datetime.datetime.strptime(
                        current_booking['departure_date'], "%d/%m/%Y").date(),
                    duration=holiday.duration,
                    total=booking_details(self.request)['subtotal']
                )
                package_booking.save()

                if username:
                    booking.user_profile = profile
                    booking.save()

                    if save_info:
                        profile_data = {
                            'default_phone_number': booking.phone_number,
                            'default_street_address1': booking.street_address1,
                            'default_street_address2': booking.street_address2,
                            'default_town_or_city': booking.town_or_city,
                            'default_county': booking.county,
                            'default_country': booking.country,
                            'default_postcode': booking.postcode,
                        }
                        user_profile_form = UserProfileForm(
                            profile_data, instance=profile)

                        if user_profile_form.is_valid():
                            user_profile_form.save()

            except Exception as e:
                if booking:
                    booking.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)


class PaypalWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handles a generic/unexpected/unknown webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["event_type"]}',
            status=200)

    def handle_payment_capture_completed(self, event):
        """
        Handles the PAYMENT.CAPTURE.COMPLETED webhook event from Paypal
        """
        return HttpResponse(
            content=f'Webhook received: {event["event_type"]}',
            status=200)
