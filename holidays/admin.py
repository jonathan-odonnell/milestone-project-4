from django.contrib import admin
from .models import Activity, Category, Country, Feature, Flight, Itinerary, Price, Package, Region


class ActivityInline(admin.StackedInline):
    model = Package.activities.through
    extra = 0
    verbose_name = 'Activity'
    verbose_name_plural = 'Activities'


class FeatureInline(admin.StackedInline):
    model = Package.features.through
    extra = 0
    verbose_name = 'Feature'
    verbose_name_plural = 'Features'


class ItineraryInline(admin.StackedInline):
    model = Itinerary
    extra = 0


class PriceInline(admin.StackedInline):
    model = Price
    extra = 0


class PackageAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline,
        FeatureInline,
        ActivityInline,
        ItineraryInline,
    ]
    exclude = ('features', 'activities', 'itinerary',)


admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Feature)
admin.site.register(Flight)
admin.site.register(Package, PackageAdmin)
admin.site.register(Region)
