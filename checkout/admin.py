from django.contrib import admin
from .models import Booking, PackageBooking


class PackageBookingAdminInline(admin.TabularInline):
    model = PackageBooking
    readonly_fields = ('package_total',)


class BookingAdmin(admin.ModelAdmin):
    inlines = (PackageBookingAdminInline,)

    readonly_fields = ('booking_number', 'date', 'total',)

    fields = ('booking_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'total',)

    list_display = ('booking_number', 'date', 'full_name',
                    'total',)

    ordering = ('-date',)

admin.site.register(Booking, BookingAdmin)