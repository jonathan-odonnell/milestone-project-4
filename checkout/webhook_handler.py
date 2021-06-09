from re import I
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import CheckoutForm
from booking.models import Booking
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
import time
import stripe


class WH_Handler:
    "Handles stripe webhooks"

    def __init__(self, request):
        self.request = request

    def send_confirmation_email(self, booking):
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

        """
        Sets any shipping details in the payment intent
        with a value of an empty string to None
        """
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Attempts to retrieve the booking every second for five seconds.
        booking_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                booking = Booking.objects.get(
                    booking_number=booking_number,
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=total,
                    paid=True,
                    stripe_pid=pid,
                )
                booking_exists = True
                break

            except Booking.DoesNotExist:
                attempt += 1
                time.sleep(1)

        """
        Sends the confirmation email and a success response
        to stripe if the booking already exists
        """
        if booking_exists:
            self.send_confirmation_email(booking)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified booking already in database',
                status=200)

        else:
            booking = None
            try:
                """
                If booking_exists remains false after 5 attempts, try and
                retreive the booking, save the checkout form and update
                the payment details in the booking
                """
                booking = Booking.objects.get(booking_number=booking_number)

                form_data = {
                    'full_name': shipping_details.name,
                    'email': billing_details.email,
                    'phone_number': shipping_details.phone,
                    'street_address1': shipping_details.address.line1,
                    'street_address2': shipping_details.address.line2,
                    'town_or_city': shipping_details.address.city,
                    'county': shipping_details.address.state,
                    'country': shipping_details.address.country,
                    'postcode': shipping_details.address.postal_code,
                }

                booking_form = CheckoutForm(form_data, instance=booking)

                if booking_form.is_valid():
                    booking = booking_form.save(commit=False)
                    booking.paid = True
                    booking.stripe_pid = pid
                    booking.save()

                """
                Saves the user's details to their profile if they were signed
                in and they checked the save_info checkbox in the form
                """
                if username != 'AnonymousUser':
                    profile = UserProfile.objects.get(user__username=username)
                    booking.update(user_profile=profile)

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

            # Sends an error response to stripe if the booking does not exist
            except Booking.DoesNotExist:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | \
                        ERROR: Booking does not exist',
                    status=500)

        """
        Sends the confirmation email and a success response
        to stripe if the booking already exists
        """
        self.send_confirmation_email(booking)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Created booking in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
