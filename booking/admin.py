from django.contrib import admin
from .models import Booking, BookingExtra, BookingPassenger, Coupon


class CouponAdmin(admin.ModelAdmin):
    """
    Code for list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    list_display = ('name', 'start_date', 'end_date', 'amount',)

    ordering = ('-end_date',)

    list_per_page = 20


class BookingExtraAdminInline(admin.TabularInline):
    """
    Code for the extra and classes is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
    """
    model = BookingExtra
    readonly_fields = ('total',)
    extra = 1
    classes = ['collapse']


class BookingPassengerAdminInline(admin.TabularInline):
    """
    Code for the extra and classes is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
    """
    model = BookingPassenger
    extra = 1
    classes = ['collapse']


class BookingAdmin(admin.ModelAdmin):
    """
    Code for list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    inlines = (BookingExtraAdminInline, BookingPassengerAdminInline)

    readonly_fields = ('booking_number', 'date', 'coupon', 'subtotal',
                       'extras_total', 'discount', 'grand_total', 'paid',
                       'stripe_pid', 'paypal_pid')

    fields = ('booking_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'street_address1', 'street_address2',
              'town_or_city',  'county', 'country', 'postcode', 'guests',
              'departure_date', 'return_date', 'package', 'outbound_flight',
              'return_flight', 'subtotal', 'coupon', 'discount',
              'extras_total', 'grand_total', 'paid', 'stripe_pid',
              'paypal_pid')

    list_display = ('booking_number', 'date', 'full_name', 'grand_total',)

    ordering = ('-date',)

    list_per_page = 20


admin.site.register(Coupon, CouponAdmin)
admin.site.register(Booking, BookingAdmin)
