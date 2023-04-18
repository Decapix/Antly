import uuid
from django.urls import reverse
from .category import *


class Product_m(models.Model):
    """The model base for any product"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=20000)
    thumbnail = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_1 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_2 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_3 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_4 = models.ImageField(upload_to="products", null=True, blank=True)
    video = models.FileField(upload_to="products", null=True, blank=True)
    problem = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("ant_detail_n", kwargs={"id": self.id})

    def __str__(self):
        return f"{self.name}"


class ProductBaseAnt_m(Product_m):
    """the model base for ant product"""
    localisation = models.CharField(choices=COUNTRY_CHOICES, max_length=50, blank=True, default="France")
    spece = models.CharField(choices=SPECE_CHOICES, max_length=100)
    under_spece = models.CharField(max_length=100, blank=True)

    def thumbnail_url(self):
        return self.thumbnail.url

    def get_location(self):
        return self.localisation

    def get_sizes(self):
        return self.sizes.all()

    def get_sizes_wiq(self):
        return self.sizes.exclude(stock=0)

    def get_price(self):
        sizes_with_stock = self.sizes.exclude(stock=0)
        if sizes_with_stock.exists():
            return sizes_with_stock.order_by('price').first().price
        else:
            return None

    def __str__(self):
        return f"{self.name}"


class Size_m(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker = models.CharField(choices=WORKER_CHOICES, max_length=20, default="5")
    gyne = models.CharField(choices=GYNE_CHOICES, max_length=20, default="1")
    stock = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_base = models.ForeignKey(ProductBaseAnt_m, on_delete=models.CASCADE, related_name='sizes', null=True,
                                     default=None)
    def info(self):
        info = {
            "thumbnail": self.product_base.thumbnail.url,
            "spece": self.product_base.spece,
            "under_spece": self.product_base.under_spece,
            "localisation": self.product_base.localisation,
            "ant": self.product_base,
            "gyne": self.gyne,
            "worker": self.worker,
        }
        return info


    def __str__(self):
        return f"{self.gyne}queen.{self.worker}w.{self.stock}stock.{self.price}€-{self.product_base}.linked"


class Pack_m(models.Model):
    """The model base for ant pack"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nest_size = models.CharField(choices=NEST_SIZE, max_length=80, default="small-plastic")
    problem = models.BooleanField(default=False)
    size = models.OneToOneField(Size_m, null=True, on_delete=models.SET_NULL)
    thumbnail_nest = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_nest_1 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_nest_2 = models.ImageField(upload_to="products", null=True, blank=True)
    video_nest = models.FileField(upload_to="products", null=True, blank=True)

    def __str__(self):
        return f"Pack - {self.size.product_base} - g{self.size.gyne} - w{self.size.worker}"

    def name(self):
        return f"Pack {self.size.product_base}"

    def get_price(self):
        return self.size.price + nest_price_f(self.nest_size)

    def thumbnail_url(self):
        info = self.size.info()
        return info.get("thumbnail")

    def spece(self):
        info = self.size.info()
        return info.get("spece")

    def complete_spece(self):
        info = self.size.info()
        return f"{info.get('spece')} {info.get('under_spece')}"

    def localisation(self):
        info = self.size.info()
        return info.get("localisation")

    def get_absolute_url(self):
        return reverse("pack_detail_n", kwargs={"id": self.id})

    def get_ant(self):
        info = self.size.info()
        return info.get("ant")


class Ant_m(ProductBaseAnt_m):
    """The model base for ant foundation"""
    Pack = models.ForeignKey(Pack_m, on_delete=models.SET_NULL, related_name='ant', null=True, blank=True, default=None)

    def __str__(self):
        return f"Ant - {self.name}"

    def get_absolute_url(self):
        return reverse("ant_detail_n", kwargs={"id": self.id})
