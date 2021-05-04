from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name',)
    list_per_page = 20


admin.site.register(Contact, ContactAdmin)
