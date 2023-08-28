import uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class Supplier_m(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    shipping_costs_parcel_supplier = models.PositiveIntegerField(default=5)
    currently_available = models.BooleanField(default=True)

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.id)

    def is_available(self):
        return self.currently_available







