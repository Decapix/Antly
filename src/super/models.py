from django.db import models

# Create your models here.


class MetaTemplate:
    def __init__(self, title, des):
        self.title = title
        self.des = des


class Offer_m(models.Model):
    """an offer"""
    active = models.BooleanField(default=False)
    message = models.CharField(max_length=100)
    text = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.message}'



