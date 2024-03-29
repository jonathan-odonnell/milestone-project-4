from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from flights.models import Flight
from extras.models import Extra
from django_extensions.db.fields import AutoSlugField
import unidecode


def slugify(name):
    """
    A function to generate the package's slug. Code is from
    https://django-extensions.readthedocs.io/en/latest/field_extensions.html
    and
    https://stackoverflow.com/questions/33328645/how-to-remove-accent-in-python-3-5-and-get-a-string-with-unicodedata-or-other-so
    """
    name = unidecode.unidecode(name)
    return name.replace(' ', '-').lower()


class Activity(models.Model):
    """ An activity model for maintaining activity information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        verbose_name_plural = 'Activities'
        ordering = ('id',)

    package = models.ForeignKey(
        'Package',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    name = models.CharField(max_length=254)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    """ A category model for maintaining category information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    name = models.CharField(max_length=254)
    slug = AutoSlugField(populate_from='name',
                         slugify_function=slugify, unique=True)
    page_title = models.CharField(max_length=254)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(models.Model):
    """ A country model for maintaining country information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Feature(models.Model):
    """ A feature model for maintaining feature information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        ordering = ('id',)

    package = models.ForeignKey(
        'Package', on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Itinerary(models.Model):
    """ An itinerary model for maintaining itinerary information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        verbose_name_plural = 'Itineraries'
        ordering = ('id',)

    package = models.ForeignKey(
        'Package',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='itineraries'
    )
    day = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    description = models.TextField()

    def __str__(self):
        return self.name


class Package(models.Model):
    """
    A package model for maintaining holiday package information
    and associated extras and flights.
    """
    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        ordering = ('id',)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='packages'
    )
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='packages'
    )
    region = models.ForeignKey(
        'Region',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='packages'
    )
    name = models.CharField(max_length=254)
    slug = AutoSlugField(populate_from='name',
                         slugify_function=slugify, unique=True)
    image = models.ImageField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    description = models.TextField()
    offer = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.DecimalField(max_digits=2, decimal_places=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    catering = models.CharField(max_length=254)
    extras = models.ManyToManyField(Extra, blank=True, related_name='packages')
    flights = models.ManyToManyField(
        Flight, blank=True, related_name='packages')
    transfers_included = models.BooleanField()

    def save(self, *args, **kwargs):
        self.slug = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Region(models.Model):
    """ A region model for maintaining region information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        ordering = ('id',)

    name = models.CharField(max_length=254)
    slug = AutoSlugField(populate_from='name',
                         slugify_function=slugify, unique=True)
    page_title = models.CharField(max_length=254)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    """ An review model for maintaining review information. """

    class Meta:
        """
        Code for default ordering is from
        https://docs.djangoproject.com/en/3.2/ref/models/options/#ordering
        """
        ordering = ('-date',)

    package = models.ForeignKey(
        'Package',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=254)
    rating = models.DecimalField(max_digits=1, decimal_places=0)
    title = models.CharField(max_length=254)
    review = models.TextField()

    def __str__(self):
        return self.title


@receiver(post_save, sender=Review)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Update the package ratings after a review is saved. Code for the Avg method
    is from
    https://docs.djangoproject.com/en/3.2/topics/db/aggregation/#cheat-sheet
    """
    instance.package.rating = instance.package.reviews.aggregate(
        Avg('rating'))['rating__avg']
    instance.package.save()
