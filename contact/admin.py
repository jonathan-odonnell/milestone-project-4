from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):

    list_display = ('subject', 'name', 'date',)
    readonly_fields = ('date',)
    fields = ('name', 'email', 'date', 'subject', 'message',)
    list_per_page = 20


admin.site.register(Contact, ContactAdmin)
