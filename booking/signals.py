from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BookingPackage, BookingExtra

@receiver(post_save, sender=BookingPackage)
def package_update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on booking package update/create
    """
    instance.booking.update_total()

@receiver(post_delete, sender=BookingPackage)
def package_update_on_delete(sender, instance, **kwargs):
    """
    Update order total on booking package delete
    """
    instance.booking.update_total()

@receiver(post_save, sender=BookingExtra)
def extra_update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on booking extras update/create
    """
    instance.booking.update_total()

@receiver(post_delete, sender=BookingExtra)
def extra_update_on_delete(sender, instance, **kwargs):
    """
    Update order total on booking extras delete
    """
    instance.booking.update_total()