from django.contrib import admin
from .models import Activity, Category, Country, Feature, Itinerary, Package, Region
from flights.models import Flight
from extras.models import Extra


class ActivityInline(admin.StackedInline):
    model = Activity
    extra = 1


class ItineraryInline(admin.StackedInline):
    model = Itinerary
    extra = 1


class PackageAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'image_url',
              'description', 'category', 'country',
              'region', 'offer', 'price', 'duration',
              'rating', 'catering', 'transfers_included',
              'features', 'extras', 'flights',)
    
    inlines = [
        ActivityInline,
        ItineraryInline,
    ]

    filter_horizontal = ('features', 'extras', 'flights')
    
    list_display = ('name', 'country', 'category',
                    'price',)

    ordering = ('country',)

    list_per_page = 20


admin.site.register(Package, PackageAdmin)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Feature)
admin.site.register(Activity)
