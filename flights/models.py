from django.db import models

class Flight(models.Model):

    class Meta:
        ordering = ('flight_number',)

    CHOICES = [
            ('', 'Direction'),
            ('Outbound', 'Outbound'),
            ('Return', 'Return'),
        ]

    flight_number = models.CharField(max_length=5, null=False, blank=False)
    direction = models.CharField(max_length=50, null=False, blank=False, choices=CHOICES)
    origin = models.CharField(max_length=50, null=False, blank=False)
    destination = models.CharField(max_length=50, null=False, blank=False)
    departure_time = models.DateTimeField(null=False, blank=False)
    arrival_time = models.DateTimeField(null=False, blank=False)
    duration = models.DurationField(null=False, blank=False)
    layover = models.CharField(max_length=50, null=True, blank=True)
    baggage = models.DecimalField(max_digits=2, decimal_places=0, null=False, blank=False)

    def __str__(self):
        return self.name
