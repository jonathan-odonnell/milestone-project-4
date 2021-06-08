from django.contrib import admin
from .models import NewsletterSignUp


class NewsletterSignUpAdmin(admin.ModelAdmin):
    """
    Code for list_per_page is from
    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options
    """
    list_per_page = 20


"""
Code to hide the sidebar and change the site header text is from
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#adminsite-attributes
"""
admin.AdminSite.enable_nav_sidebar = False
admin.AdminSite.site_header = 'Go Explore Admin'
admin.site.register(NewsletterSignUp, NewsletterSignUpAdmin)
