from django.contrib import admin
from .models import (Activity, Category, Country, Feature,
                     Itinerary, Package, Region, Review)


class ActivityInline(admin.StackedInline):
    """
    Code for the stacked inline, extra and classes is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
    """
    model = Activity
    extra = 1
    classes = ['collapse']


class FeatureInline(admin.StackedInline):
    """
    Code for the stacked inline, extra and classes is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
    """
    model = Feature
    extra = 1
    classes = ['collapse']


class ItineraryInline(admin.StackedInline):
    """
    Code for the stacked inline, extra and classes is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
    """
    model = Itinerary
    extra = 1
    classes = ['collapse']


class PackageAdmin(admin.ModelAdmin):
    """
    Code for filter_horizontal, list_filter and list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    readonly_fields = ('rating',)

    fields = ('name', 'image', 'image_url',
              'description', 'category', 'country',
              'region', 'offer', 'price', 'duration',
              'rating', 'catering', 'transfers_included',
              'extras', 'flights',)

    inlines = [
        FeatureInline,
        ActivityInline,
        ItineraryInline,
    ]

    filter_horizontal = ('extras', 'flights')

    list_display = ('name', 'country', 'category', 'price',)

    list_filter = ('category', 'country')

    ordering = ('country', 'name')

    list_per_page = 20


class ReviewAdmin(admin.ModelAdmin):
    """
    Code for list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    readonly_fields = ('date',)

    fields = ('full_name', 'date', 'package', 'rating', 'title', 'review',)

    list_display = ('title', 'full_name', 'package', 'date',)

    ordering = ('-date',)

    list_per_page = 20


admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Package, PackageAdmin)
admin.site.register(Region)
admin.site.register(Review, ReviewAdmin)
