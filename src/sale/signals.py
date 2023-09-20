from django.db.models.signals import post_save
from django.dispatch import receiver
from .modelcart import OrderTrack_m
from .extras import send_tracking_number_email
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=OrderTrack_m)
def send_tracking_email(sender, instance, **kwargs):
    order = instance.order
    latest_order_track = instance.order_track
    
    if order and order.owner:
        send_tracking_number_email(order, latest_order_track)
