from django.db import models


class NewsletterSignUp(models.Model):
    """
    A newsletter sign up model for maintaining email addresses signed up
    to the newsletter.
    """
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email
