from django.db import models
from extras.models import Extra
from django_extensions.db.fields import AutoSlugField

def slugify(content):
    """
    A function to generate the package's slug. Code is from 
    https://django-extensions.readthedocs.io/en/latest/field_extensions.html
    """
    return content.replace(' ', '-').lower()


class Activity(models.Model):

    class Meta:
        verbose_name_plural = 'Activities'

    activity = models.CharField(max_length=254)
    description = models.TextField()

    def __str__(self):
        return self.activity


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    page_title = models.CharField(max_length=254)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', slugify_function=slugify)

    def __str__(self):
        return self.name


class Country(models.Model):

    class Meta:
        verbose_name_plural = 'Countries'

    name = models.CharField(max_length=254)
    region = models.ForeignKey('Region', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Feature(models.Model):

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


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


class Itinerary(models.Model):

    class Meta:
        verbose_name_plural = 'Itineraries'

    days = (
        ('1', 'Day 1'),
        ('2', 'Day 2'),
        ('3', 'Day 3'),
        ('4', 'Day 4'),
        ('5', 'Day 5'),
        ('6', 'Day 6'),
        ('7', 'Day 7'),
        ('8', 'Day 8'),
        ('9', 'Day 9'),
        ('10', 'Day 10'),
    )

    title = models.CharField(max_length=254)
    description = models.TextField()
    package = models.ForeignKey('Package', null=True, blank=True, on_delete=models.CASCADE)
    day = models.CharField(choices=days, max_length=2)

    def __str__(self):
        return self.title


class Package(models.Model):

    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(
        'Country', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    duration = models.DecimalField(max_digits=2, decimal_places=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    catering = models.CharField(max_length=254)
    features = models.ManyToManyField('Feature')
    activities = models.ManyToManyField('Activity')
    extras = models.ManyToManyField(Extra, related_name='packages')
    outbound_flight = models.ForeignKey(
        'Flight', null=True, blank=True, on_delete=models.SET_NULL, related_name='outbound_flight')
    return_flight = models.ForeignKey(
        'Flight', null=True, blank=True, on_delete=models.SET_NULL, related_name='inbound_flight')
    transfers_included = models.BooleanField()
    slug = AutoSlugField(populate_from='name', slugify_function=slugify)

    def __str__(self):
        return self.name


class Price(models.Model):
    
    package = models.ForeignKey(
        'Package', null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    offer = models.BooleanField()

    def __str__(self):
        return "{} {} - {}".format(self.package, self.start_date, self.end_date)


class Region(models.Model):

    name = models.CharField(max_length=254)
    page_title = models.CharField(max_length=254)
    image = models.ImageField()
    image_url = models.CharField(max_length=254, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', slugify_function=slugify)

    def __str__(self):
        return self.name
