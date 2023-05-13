from django.db import models
from user.models import Shopper_m as Profile
from user.models import Address_m as Address
from .models import *
from .extras import send_tracking_number_email
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# cart


class OrderItem_m(models.Model):
    """for ant product"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProductBaseAnt_m, on_delete=models.SET_NULL, null=True)
    pack = models.ManyToManyField(Pack_m, blank=True, null=True)
    size = models.ManyToManyField(Size_m)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def name(self):
        return f'Pack {self.product}' if self.pack.exists() else f'{self.product}'

    def get_absolute_url(self):
        if self.pack.exists():
            return self.pack.first().get_absolute_url()
        else:
            return self.product.get_absolute_url()

    def __str__(self):
        return 'Pack {0} - {1}'.format(self.owner, self.product) if self.pack.exists() else 'Ant {0} - {1}'.format(self.owner, self.product)


class Order_m(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=15, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem_m)
    date_ordered = models.DateTimeField(auto_now=True)
    address = models.OneToOneField(Address, null=True, on_delete=models.SET_NULL)
    order_track = models.CharField(max_length=30, null=True, blank=True)


    def shipping_costs(self):
        return 0 if settings.FREE_SHIPPING_COSTE else 5

    def gift(self):
        if settings.FREE_COLONIE:
            n = sum(item.quantity for item in self.items.all() if item.is_ordered == False)
            if n >= 3:
                return True
        return False

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return int(self.shipping_costs()) + sum(item.quantity * item.price for item in self.items.all() if item.is_ordered == False)

    def get_order_total(self):
        return int(self.shipping_costs()) + sum(
            item.quantity * item.price for item in self.items.all() if item.is_ordered == True)

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shopper = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    order = models.OneToOneField(Order_m, on_delete=models.CASCADE)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.shopper} - {self.order}"

    class Meta:
        ordering = ['-timestamp']


@receiver(post_save, sender=Order_m)
def send_tracking_number(sender, instance, **kwargs):
    if instance.order_track:  # Vérifie si le numéro de suivi n'est pas vide
        send_tracking_number_email(instance)
