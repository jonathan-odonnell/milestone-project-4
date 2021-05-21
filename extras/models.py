from django.db import models
from django_extensions.db.fields import AutoSlugField


def slugify(content):
    """
    A function to generate the package's slug. Code is from 
    https://django-extensions.readthedocs.io/en/latest/field_extensions.html
    """
    return content.replace(' ', '-').lower()


class Extra(models.Model):

    class Meta:
        ordering = ('id',)

    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', slugify_function=slugify)

    def __str__(self):
        return f'{self.name} - £{self.price}'
