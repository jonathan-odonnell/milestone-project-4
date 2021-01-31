import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from holidays.models import Package

class Booking(models.Model):
    booking_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    coupon = models.CharField(max_length=20, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_booking_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        self.total = self.package_booking.total
        self.save()

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number

class PackageBooking(models.Model):
    booking = models.OneToOneField(Booking, null=False, blank=False, on_delete=models.CASCADE, related_name='package_booking')
    package = models.ForeignKey(Package, null=False, blank=False, on_delete=models.CASCADE)
    guests = models.IntegerField(null=False, blank=False)
    departure_date = models.DateField(null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)
    total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def __str__(self):
        return f'{self.package.name} on booking {self.booking.booking_number}'
