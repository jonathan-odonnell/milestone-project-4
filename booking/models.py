from django.db import models
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from profiles.models import UserProfile
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra
import datetime

class Coupon(models.Model):
    
    name = models.CharField(max_length=254)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{} {} - {}".format(self.name, self.start_date, self.end_date)


class Booking(models.Model):
    booking_number = models.CharField(
        max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='bookings')
    email = models.EmailField(max_length=254, null=False, blank=False, default='')
    phone_number = models.CharField(max_length=20, null=False, blank=False, default='')
    town_or_city = models.CharField(max_length=40, null=False, blank=False, default='')
    street_address1 = models.CharField(max_length=80, null=False, blank=False, default='')
    street_address2 = models.CharField(max_length=80, null=True, blank=True, default='')
    county = models.CharField(max_length=80, null=False, blank=False, default='')
    country = CountryField(blank_label='Country *', null=False, blank=False, default='')
    postcode = models.CharField(max_length=20, null=False, blank=False, default='')
    date = models.DateTimeField(auto_now_add=True)
    coupon = models.CharField(max_length=20, null=True, blank=True)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    extras_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0, editable=False)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    paid = models.BooleanField(null=False, blank=False, default=False, editable=False)
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')
    paypal_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_booking_number(self):
        return uuid.uuid4().hex.upper()

    def update_totals(self):
        package_total = self.booking_package.total
        extras_total = self.booking_extras.aggregate(Sum('total'))[
            'total__sum'] or 0
        self.subtotal = package_total
        self.extras_total = extras_total
        self.total = package_total + extras_total - self.discount
        self.save()

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        if self.coupon:
            coupon_qs = Coupon.objects.get(name=self.coupon)
            self.discount = coupon_qs.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number


class BookingPackage(models.Model):
    booking = models.OneToOneField(
        Booking, null=False, blank=False, on_delete=models.CASCADE, related_name='booking_package')
    package = models.ForeignKey(
        Package, null=False, blank=False, on_delete=models.CASCADE)
    guests = models.IntegerField(null=False, blank=False)
    departure_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=False, blank=False)
    outbound_flight = models.ForeignKey(
        Flight, null=True, blank=True, on_delete=models.SET_NULL, related_name='booking_outbound_flight')
    return_flight = models.ForeignKey(
        Flight, null=True, blank=True, on_delete=models.SET_NULL, related_name='booking_inbound_flight')
    total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.package.price * self.guests
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.package.name} on booking {self.booking.booking_number}'


class BookingExtra(models.Model):
    booking = models.ForeignKey(
        Booking, null=False, blank=False, on_delete=models.CASCADE, related_name='booking_extras')
    extra = models.ForeignKey(
        Extra, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.extra.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.extra.name} on booking {self.booking.booking_number}'


class BookingPassenger(models.Model):
    booking = models.ForeignKey(
        Booking, null=False, blank=False, on_delete=models.CASCADE, related_name='booking_passengers')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    passport_number = models.DecimalField(max_digits=9, decimal_places=0, null=False, blank=False)

    def __str__(self):
        return f'{self.full_name} on booking {self.booking.booking_number}'
