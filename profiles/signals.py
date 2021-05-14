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
    Create or update the user profile and create stripe customer
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


@receiver(post_save, sender=UserProfile)
def update_user_email(sender, instance, created, **kwargs):
    """
    Updates the email address
    """
    if not created:
        email = EmailAddress.objects.filter(user=instance.user)
        email.update(email=instance.user.email, primary=True)

@receiver(post_save, sender=UserProfile)
def stripe_update_on_save(sender, instance, created, **kwargs):
    """
    Update stripe customer details on update
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
