from django.db import models


class CustomerContact(models.Model):
    """
    Code for direction choices is from
    https://docs.djangoproject.com/en/3.2/ref/models/fields/#choices
    """
    SUBJECT_CHOICES = [
        ('', 'Subject'),
        ('Holiday Information', 'Holiday Information'),
        ('Offers', 'Offers'),
        ('Bookings', 'Bookings'),
        ('General Enquiries', 'General Enquiries'),
        ('Other', 'Other')
    ]

    full_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=254, choices=SUBJECT_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f'{self.full_name} - {self.subject}'
