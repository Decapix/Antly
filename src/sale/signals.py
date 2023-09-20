from django.db.models.signals import post_save
from django.dispatch import receiver
from .modelcart import OrderTrack_m
from .extras import send_tracking_number_email
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=OrderTrack_m)
def send_tracking_number(sender, instance, created, **kwargs):
    if created:  # Vérifie si le numéro de suivi n'est pas vide
        order = instance.order
        latest_order_track = OrderTrack_m.objects.filter(order=order).last()
        send_tracking_number_email(order, latest_order_track)