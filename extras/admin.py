from django.contrib import admin
from .models import Extra


class ExtraAdmin(admin.ModelAdmin):
    """
    Code for list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    list_display = ('name', 'price',)
    list_per_page = 20


admin.site.register(Extra, ExtraAdmin)
