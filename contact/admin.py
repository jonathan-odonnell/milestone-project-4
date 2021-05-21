from django.contrib import admin
from .models import CustomerContact

class CustomerContactAdmin(admin.ModelAdmin):

    list_display = ('subject', 'full_name', 'date',)
    readonly_fields = ('date',)
    fields = ('full_name', 'email', 'date', 'subject', 'message',)
    ordering = ('-date',)
    list_per_page = 20


admin.site.register(CustomerContact, CustomerContactAdmin)
