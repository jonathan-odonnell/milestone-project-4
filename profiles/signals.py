from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
import stripe


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates the user profile and creates a stripe customer
    when a user profile is created. Code is from
    https://stripe.com/docs/api/accounts/create
    """
    if created:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        UserProfile.objects.create(user=instance)
        customer = stripe.Customer.create(
            name=instance.get_full_name(),
            email=instance.email
        )
        instance.userprofile.stripe_customer_id = customer['id']
    instance.userprofile.save()


@receiver(post_save, sender=User)
def update_user_email(sender, instance, created, **kwargs):
    """
    Updates the email address in the allauth email address database
    and sends the verification email. Code is from
    https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py
    """
    if not created:
        existing_email = EmailAddress.objects.get(user=instance)

        if existing_email and existing_email.email != instance.email:
            EmailAddress.objects.create(
                email=instance.email, user=instance, primary=True)
            existing_email.delete()


@receiver(post_save, sender=UserProfile)
def stripe_update_on_save(sender, instance, created, **kwargs):
    """
    Update stripe customer details on when the user profile is updated.
    Code is from https://stripe.com/docs/api/accounts/update
    """
    if not created:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.Customer.modify(
            instance.stripe_customer_id,
            email=instance.user.email,
            address={
                'line1': instance.street_address1,
                'line2': instance.street_address2,
                'city': instance.town_or_city,
                'state': instance.county,
                'country': instance.country,
                'postal_code': instance.postcode
            }
        )
