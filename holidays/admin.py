from django.contrib import admin
from .models import Activity, Category, Country, Feature, Itinerary, Price, Package, Region
from flights.models import Flight
from extras.models import Extra


class ItineraryInline(admin.StackedInline):
    model = Itinerary
    extra = 0


class PriceInline(admin.StackedInline):
    model = Price
    extra = 0


class PackageAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline,
        ItineraryInline,
    ]
    filter_horizontal = ('features', 'activities', 'extras', 'flights')


admin.site.register(Package, PackageAdmin)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Feature)
admin.site.register(Activity)
