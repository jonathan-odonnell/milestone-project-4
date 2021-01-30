from django.db import models

class Coupon(models.Model):
    
    name = models.CharField(max_length=254)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{} {} - {}".format(self.name, self.start_date, self.end_date)
