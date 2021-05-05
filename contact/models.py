from django.db import models


class Contact(models.Model):

    SUBJECTS = [
            ('', 'Subject *'),
            ('Holiday Information', 'Holiday Information'),
            ('Offers', 'Offers'),
            ('Bookings', 'Bookings'),
            ('General Enquiries', 'General Enquiries'),
            ('Other', 'Other')
        ]

    name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=254, choices=SUBJECTS)
    message = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.subject}'
