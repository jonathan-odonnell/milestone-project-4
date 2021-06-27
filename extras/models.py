from django.db import models
from django_extensions.db.fields import AutoSlugField


class Extra(models.Model):
    """
    An extra model for maintaining extra information. Code for the slug field
    is from
    https://django-extensions.readthedocs.io/en/latest/field_extensions.html
    """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        ordering = ('id',)

    name = models.CharField(max_length=254)
    slug = AutoSlugField(populate_from='name', unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - £{self.price}'
