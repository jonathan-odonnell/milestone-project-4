from django.contrib import admin
from .models import Activity, Category, Country, Feature, Itinerary, Package, Region, Review
from flights.models import Flight
from extras.models import Extra


class ActivityInline(admin.StackedInline):
    model = Activity
    extra = 1


class FeatureInline(admin.StackedInline):
    model = Feature
    extra = 1


class ItineraryInline(admin.StackedInline):
    model = Itinerary
    extra = 1

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1
    fields = ('full_name', 'rating', 'title', 'review',)


class PackageAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'image_url',
              'description', 'category', 'country',
              'region', 'offer', 'price', 'duration',
              'rating', 'catering', 'transfers_included', 
              'extras', 'flights',)
    
    inlines = [
        FeatureInline,
        ActivityInline,
        ItineraryInline,
        ReviewInline,
    ]

    filter_horizontal = ('extras', 'flights')
    
    list_display = ('name', 'country', 'category',
                    'price',)

    ordering = ('country', 'name')

    list_per_page = 20


admin.site.register(Package, PackageAdmin)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Region)
