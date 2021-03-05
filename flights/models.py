from django.db import models

class Flight(models.Model):

    name = models.CharField(max_length=6)
    origin = models.CharField(max_length=254)
    destination = models.CharField(max_length=254)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    layover = models.CharField(max_length=254, null=True, blank=True)
    baggage = models.DecimalField(max_digits=2, decimal_places=0)

    def __str__(self):
        return self.name
