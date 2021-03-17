from django.http import HttpResponse
from booking.models import Booking, BookingPackage
from holidays.models import Package
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from booking.contexts import booking_details
import time
import datetime
import stripe


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
        stripe.api_key = settings.STRIPE_SECRET_KEY
        booking_number = intent.metadata.booking_number
        save_info = intent.metadata.save_info
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
                    booking_number=booking_number,
                    total=total,
                    paid=True,
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
                booking = Booking.objects.get(booking_number=booking_number)
                booking.update(
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    town_or_city=billing_details.address.city,
                    county=billing_details.address.state,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    paid=True,
                    stripe_pid=pid,
                )
                booking.save()

                if username:
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
                            profile.save()

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
