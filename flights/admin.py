from django.contrib import admin
from .models import Flight


class FlightAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin', 'destination',)

    ordering = ('name',)

    list_per_page = 20

admin.site.register(Flight, FlightAdmin)
