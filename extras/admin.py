from django.contrib import admin
from .models import Extra


class ExtraAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    list_per_page = 20


admin.site.register(Extra, ExtraAdmin)
