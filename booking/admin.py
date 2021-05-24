from django.contrib import admin
from .models import Booking, BookingExtra, BookingPassenger, Coupon


class BookingExtraAdminInline(admin.TabularInline):
    model = BookingExtra
    readonly_fields = ('total',)


class BookingPassengerAdminInline(admin.TabularInline):
    model = BookingPassenger


class BookingAdmin(admin.ModelAdmin):
    inlines = (BookingExtraAdminInline, BookingPassengerAdminInline)

    readonly_fields = ('booking_number', 'date', 'coupon', 'subtotal',
                       'extras_total', 'discount', 'grand_total', 'paid',
                       'stripe_pid', 'paypal_pid')

    fields = ('booking_number', 'user_profile', 'date', 
              'full_name', 'email', 'phone_number',
              'street_address1', 'street_address2',
              'town_or_city',  'county', 'postcode', 
              'country', 'guests', 'departure_date', 
              'return_date', 'package', 'outbound_flight', 
              'return_flight', 'subtotal', 'coupon', 'discount', 
              'extras_total', 'grand_total', 'paid', 'stripe_pid',
              'paypal_pid')

    list_display = ('booking_number', 'date', 'full_name',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Coupon)
admin.site.register(Booking, BookingAdmin)
