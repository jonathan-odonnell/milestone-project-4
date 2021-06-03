from django.contrib import admin
from .models import Flight


class FlightAdmin(admin.ModelAdmin):
    readonly_fields = ('duration',)

    fields = (
        'flight_number', 'direction', 'origin', 
        'destination', 'departure_time', 'origin_time_zone',
        'arrival_time', 'destination_time_zone', 'duration',
        'layover', 'baggage')
    
    list_display = ('flight_number', 'origin', 'destination',)
    
    ordering = ('flight_number',)
    
    list_per_page = 20

admin.site.register(Flight, FlightAdmin)
