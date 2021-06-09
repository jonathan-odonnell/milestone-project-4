from django.contrib import admin
from .models import CustomerContact


class CustomerContactAdmin(admin.ModelAdmin):
    """
    Code for list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    list_display = ('subject', 'full_name', 'date',)

    readonly_fields = ('date',)

    fields = ('full_name', 'email', 'date', 'subject', 'message',)

    ordering = ('-date',)

    list_per_page = 20


admin.site.register(CustomerContact, CustomerContactAdmin)
