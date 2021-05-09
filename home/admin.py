from django.contrib import admin
from .models import NewsletterSignUp


class NewsletterSignUpAdmin(admin.ModelAdmin):

    list_per_page = 20


admin.site.register(NewsletterSignUp, NewsletterSignUpAdmin)
