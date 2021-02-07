from django.contrib import admin
from .models import Activity, Category, Country, Feature, Flight, Itinerary, Price, Package, Region
from extras.models import Extra


class ActivityInline(admin.StackedInline):
    model = Package.activities.through
    extra = 0
    verbose_name = 'Activity'
    verbose_name_plural = 'Activities'


class ExtraInline(admin.StackedInline):
    model = Package.extras.through
    extra = 0
    verbose_name = 'Extra'
    verbose_name_plural = 'Extras'


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
        ExtraInline,
        FeatureInline,
        ActivityInline,
        ItineraryInline,
    ]
    exclude = ('features', 'activities', 'extras')


admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Extra)
admin.site.register(Feature)
admin.site.register(Flight)
admin.site.register(Package, PackageAdmin)
admin.site.register(Region)
