from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from timezone_field import TimeZoneField
import pytz

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
        if self.direction == 'Outbound':
            tz = self.destination_time_zone
            self.arrival_time = self.arrival_time.replace(tzinfo=None)
            self.arrival_time = tz.localize(self.arrival_time)
            self.arrival_time = self.arrival_time.astimezone(pytz.utc)
        else:
            tz = self.origin_time_zone
            self.departure_time = self.departure_time.replace(tzinfo=None)
            self.departure_time = tz.localize(self.departure_time)
            self.departure_time = self.departure_time.astimezone(pytz.utc)
        self.duration = self.arrival_time - self.departure_time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.flight_number
