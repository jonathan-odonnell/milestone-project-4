from django.contrib import admin
from .models import Activity, Category, Country, Feature, Flight, Itinerary, Price, Package


admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Feature)
admin.site.register(Flight)
admin.site.register(Package)
