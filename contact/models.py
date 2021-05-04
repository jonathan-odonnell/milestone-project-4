from django.db import models


class Contact(models.Model):

    name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.subject}'
