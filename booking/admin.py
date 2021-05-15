from django.contrib import admin
from .models import Booking, BookingPackage, BookingExtra, BookingPassenger, Coupon


class BookingPackageAdminInline(admin.StackedInline):
    model = BookingPackage
    readonly_fields = ('total',)


class BookingExtraAdminInline(admin.TabularInline):
    model = BookingExtra
    readonly_fields = ('total',)


class BookingPassengerAdminInline(admin.TabularInline):
    model = BookingPassenger


class BookingAdmin(admin.ModelAdmin):
    inlines = (BookingPackageAdminInline, BookingExtraAdminInline, BookingPassengerAdminInline)

    readonly_fields = ('booking_number', 'date', 'coupon', 'subtotal',
                       'extras_total', 'discount', 'grand_total', 'paid',
                       'stripe_pid', 'paypal_pid')

    fields = ('booking_number', 'user_profile', 'date', 
              'full_name', 'email', 'phone_number',
              'street_address1', 'street_address2',
              'town_or_city',  'country', 'postcode', 
              'county', 'coupon', 'subtotal', 'discount', 
              'extras_total', 'grand_total', 'paid', 'stripe_pid',
              'paypal_pid')

    list_display = ('booking_number', 'date', 'full_name',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Coupon)
admin.site.register(Booking, BookingAdmin)
