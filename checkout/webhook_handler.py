from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from booking.models import Booking, BookingPackage
from holidays.models import Package
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
import time
import datetime
import stripe


class StripeWH_Handler:
    "Handles stripe webhooks"

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, booking):
        """Send the user a confirmation email"""
        cust_email = booking.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'booking': booking})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'booking': booking, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )       

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
        shipping_details = intent.shipping
        total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        booking_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                booking = Booking.objects.get(
                    booking_number=booking_number,
                    grand_total=total,
                    paid=True,
                    stripe_pid=pid,
                )
                booking_exists = True
                break

            except Booking.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if booking_exists:
            self._send_confirmation_email(booking)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified booking already in database',
                status=200)

        else:
            booking = None
            try:
                booking = Booking.objects.filter(booking_number=booking_number)
                booking.update(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    town_or_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    paid=True,
                    stripe_pid=pid,
                )

                if username:
                    booking.update(user_profile=profile)

                    if save_info:
                        profile_data = {
                            'phone_number': booking[0].phone_number,
                            'street_address1': booking[0].street_address1,
                            'street_address2': booking[0].street_address2,
                            'town_or_city': booking[0].town_or_city,
                            'county': booking[0].county,
                            'country': booking[0].country,
                            'postcode': booking[0].postcode,
                        }
                        user_profile_form = UserProfileForm(
                            profile_data, instance=profile)

                        if user_profile_form.is_valid():
                            user_profile_form.save()

            except Booking.DoesNotExist:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: Booking does not exist',
                    status=500)

        self._send_confirmation_email(booking)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created booking in webhook',
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
