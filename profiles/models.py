from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField
import stripe


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=False, blank=False)
    country = CountryField(blank_label='Country', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    stripe_customer_id = models.CharField(
        max_length=254, null=True, blank=True)

    def get_address(self, *args, **kwargs):
        if self.street_address2:
            return f'{self.street_address1} {self.street_address2}'
        else:
            return f'{self.street_address1}'

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = stripe.Customer.create()
        UserProfile.objects.create(
            user=instance, stripe_customer_id=customer.id)
    instance.userprofile.save()

    if not created and UserProfile.stripe_customer_id:
        stripe.Customer.modify(
            UserProfile.stripe_customer_id,
            name=UserProfile.user.get_full_name(),
            email=UserProfile.user.email,
            address={
                'line1': UserProfile.street_address1,
                'line2': UserProfile.street_address2,
                'city': UserProfile.town_or_city,
                'state': UserProfile.county,
                'country': UserProfile.country,
                'postal_code': UserProfile.postcode,
            }
        )
