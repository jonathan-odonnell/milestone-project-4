from django.db import models
from timezone_field import TimeZoneField
from django.utils import timezone


class Flight(models.Model):

    class Meta:
        ordering = ('flight_number',)

    CHOICES = [
        ('', 'Direction'),
        ('Outbound', 'Outbound'),
        ('Return', 'Return'),
    ]

    flight_number = models.CharField(max_length=5)
    direction = models.CharField(max_length=50, choices=CHOICES)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    origin_time_zone = TimeZoneField()
    arrival_time = models.DateTimeField()
    destination_time_zone = TimeZoneField()
    duration = models.DurationField()
    layover = models.CharField(max_length=50, null=True, blank=True)
    baggage = models.DecimalField(max_digits=2, decimal_places=0)

    def save(self, *args, **kwargs):
        """
        Converts departure time and arrival time to the user's local timezone
        and calculates he flight duration when the model is saved. Code for converting 
        the timezones is from 
        https://stackoverflow.com/questions/36122619/manually-setting-time-zone-in-django-form
        and https://docs.djangoproject.com/en/3.2/topics/i18n/timezones/
        """
        current_time_zone = timezone.get_current_timezone()
        arrival_time = self.arrival_time.replace(tzinfo=None)
        arrival_time = self.destination_time_zone.localize(arrival_time)
        self.arrival_time = current_time_zone.normalize(
            arrival_time.astimezone(current_time_zone))
        departure_time = self.departure_time.replace(tzinfo=None)
        departure_time = self.origin_time_zone.localize(departure_time)
        self.departure_time = current_time_zone.normalize(
            departure_time.astimezone(current_time_zone))
        self.duration = self.arrival_time - self.departure_time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.flight_number
