from django.contrib import admin
from .models import Flight


class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination',)

    ordering = ('flight_number',)

    list_per_page = 20

admin.site.register(Flight, FlightAdmin)
