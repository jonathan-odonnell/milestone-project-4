from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from timezone_field import TimeZoneField

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
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    destination_time_zone = TimeZoneField()
    layover = models.CharField(max_length=50, null=True, blank=True)
    baggage = models.DecimalField(max_digits=2, decimal_places=0)

    def __str__(self):
        return self.flight_number
