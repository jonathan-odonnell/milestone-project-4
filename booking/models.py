from django.db import models
import uuid
from django.db.models import Sum
from django.db.models.deletion import SET_NULL
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from profiles.models import UserProfile
from holidays.models import Package
from flights.models import Flight
from extras.models import Extra


class Coupon(models.Model):

    name = models.CharField(max_length=254)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} {self.start_date} - {self.end_date}'


class Booking(models.Model):
    """
    Code for the PhoneNumberField is from
    https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    """
    booking_number = models.CharField(max_length=32)
    full_name = models.CharField(max_length=50, default='')
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='bookings')
    email = models.EmailField(max_length=254, default='')
    phone_number = PhoneNumberField(max_length=20, default='')
    street_address1 = models.CharField(max_length=80, default='')
    street_address2 = models.CharField(
        max_length=80, null=True, blank=True, default='')
    town_or_city = models.CharField(max_length=40, default='')
    county = models.CharField(max_length=80, default='')
    country = CountryField(blank_label='Country *', default='')
    postcode = models.CharField(max_length=20, default='')
    date = models.DateTimeField(auto_now_add=True)
    guests = models.IntegerField(default=0)
    departure_date = models.DateField()
    return_date = models.DateField()
    package = models.ForeignKey(
        Package, null=True, blank=True, on_delete=SET_NULL)
    outbound_flight = models.ForeignKey(
        Flight, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='outbound_flight')
    return_flight = models.ForeignKey(
        Flight, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='return_flight')
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0)
    extras_total = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0)
    coupon = models.CharField(max_length=20, null=True,
                              blank=True, editable=False)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0)
    paid = models.BooleanField(editable=False, default=False)
    stripe_pid = models.CharField(max_length=254, default='')
    paypal_pid = models.CharField(max_length=254, default='')

    def _generate_booking_number(self):
        return uuid.uuid4().hex.upper()

    def update_totals(self):
        self.extras_total = self.booking_extras.aggregate(Sum('total'))[
            'total__sum'] or 0
        self.grand_total = self.subtotal + self.extras_total - self.discount
        self.save()

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        if self.coupon:
            coupon_qs = Coupon.objects.get(name=self.coupon)
            self.discount = coupon_qs.amount
        self.subtotal = self.package.price * self.guests
        self.grand_total = self.subtotal + self.extras_total - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number


class BookingExtra(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='booking_extras')
    extra = models.ForeignKey(
        Extra, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.extra.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.extra.name} on booking {self.booking.booking_number}'


class BookingPassenger(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='booking_passengers')
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    passport_number = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        return f'{self.full_name} on booking {self.booking.booking_number}'
