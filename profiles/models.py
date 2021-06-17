from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default contact information
    and order history. Code for the PhoneNumberField is from
    https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    stripe_customer_id = models.CharField(
        max_length=254, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()
