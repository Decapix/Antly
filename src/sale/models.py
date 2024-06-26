import os
import uuid
from django.urls import reverse
from .category import *
from PIL import Image
from io import BytesIO
from django.core.files import File
from admin_supplier.models import Supplier_m
from django.db import models
from django.db import models
from django.core.files.base import ContentFile



# Mixin pour la conversion d'image
class ImageConversionMixin:
    def convert_image_to_webp(self, image_field):
        if image_field and not image_field.name.endswith('.webp'):
            # Ouvrir l'image originale
            pil_image = Image.open(image_field)
            # Convertir l'image en WebP
            if pil_image.mode in ("RGBA", "P"):
                pil_image = pil_image.convert("RGB")
            output_io_stream = BytesIO()
            pil_image.save(output_io_stream, format='WEBP', quality=90)
            webp_image = ContentFile(output_io_stream.getvalue(), os.path.splitext(image_field.name)[0] + '.webp')
            
            # Sauvegarder l'image WebP
            image_field.save(webp_image.name, webp_image, save=False)

    def save(self, *args, **kwargs):
        # Convertir toutes les images en WebP
        self.convert_image_to_webp(self.thumbnail)
        for i in range(1, 5):
            thumbnail_field = getattr(self, f'thumbnail_{i}', None)
            if thumbnail_field:
                self.convert_image_to_webp(thumbnail_field)
        
        super().save(*args, **kwargs)  # Appeler la méthode save() du parent

class Product_m(ImageConversionMixin, models.Model):
    """The model base for any product"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    thumbnail = models.ImageField(upload_to="products")
    thumbnail_1 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_2 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_3 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_4 = models.ImageField(upload_to="products", null=True, blank=True)
    video = models.FileField(upload_to="products", null=True, blank=True)
    problem = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name}"

    def sh_description(self):
        return self.description

    def sh_problem(self):
        return self.problem

    def thumbnail_url(self):
        return self.thumbnail.url
    

    """ def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

        thumbnails = [
            self.thumbnail,
            self.thumbnail_1,
            self.thumbnail_2,
            self.thumbnail_3,
            self.thumbnail_4,
        ]

        for thumbnail in thumbnails:
            if thumbnail and thumbnail.name and thumbnail.file:  # check if the thumbnail exists, has a name, and has a file
                try:
                    img = Image.open(thumbnail.path)  # open the image

                    output_io = BytesIO()
                    img.resize((1040, 880)).convert('RGB').save(output_io, format='WEBP',
                                                               quality=70)  # resize and convert to WebP
                    output_io.seek(0)

                    # Change the file extension to .webp
                    thumbnail_name = f'{os.path.splitext(thumbnail.name)[0]}.webp'

                    thumbnail.delete(save=False)
                    thumbnail.save(thumbnail_name, File(output_io), save=False)
                except Exception as e:
                    print(f"Error processing image: {e}")

        super().save(*args, **kwargs)  # Call the "real" save() method again. """


class Ant_m(Product_m):
    """The model base for ant foundation"""
    localisation = models.CharField(choices=COUNTRY_CHOICES, max_length=50, blank=True, default="France")
    spece = models.CharField(choices=SPECE_CHOICES, max_length=100)
    under_spece = models.CharField(max_length=100, blank=True)
    supplier = models.ForeignKey(Supplier_m, on_delete=models.CASCADE, related_name='ant', null=True, blank=True,
                                 default=None)

    def __str__(self):
        return f"Ant - {self.name} / {self.supplier}"

    def sh_name(self):
        return f"{self.name}"

    def sh_spece(self):
        return self.spece

    def get_absolute_url(self):
        return reverse("ant_detail_n", kwargs={"id": self.id})

    def sh_localisation(self):
        return self.localisation

    def get_sizes(self):
        return self.sizes.all()

    def get_sprice(self, price):
        for y in self.get_sizes():
            if y.price == price :
                return y

    def get_sizes_wiq(self):
        return self.sizes.exclude(stock=0)

    def sh_price(self):
        sizes_with_stock = self.sizes.exclude(stock=0)
        if sizes_with_stock.exists():
            return sizes_with_stock.order_by('price').first().price
        else:
            return None

    def check_stock(self, quantity, size):
        """checker la quantitée
            return True → tout va bien , on a assez de stock
            return x → il nous reste x unitées en stock
        """
        return True if int(size.stock) - int(quantity) >= 0 else int(size.stock)

    def get_stock(self, size):
        return int(size.stock)

    def sh_supplier(self):
        return self.supplier.name

    def show_supplier_id(self):
        return self.supplier.id





class Size_m(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker = models.CharField(choices=WORKER_CHOICES, max_length=20, default="5")
    gyne = models.CharField(choices=GYNE_CHOICES, max_length=20, default="1")
    stock = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_base = models.ForeignKey(Ant_m, on_delete=models.CASCADE, related_name='sizes', null=True,
                                     default=None)
    supplier = models.ForeignKey(Supplier_m, on_delete=models.CASCADE, related_name='sizes', null=True, blank=True,
                                     default=None)


    def __str__(self):
        return f"{self.gyne}queen.{self.worker}w.{self.stock}stock.{self.price}€-{self.product_base}.linked"

    def is_available(self):
        return self.supplier.is_available()

    def sh_supplier(self):
        return self.supplier.name

    def show_supplier_id(self):
        return self.supplier.id


class Other_m(Product_m):
    """The model base for other product"""

    stock = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(choices=TYPE_CHOICES, max_length=50, blank=True, default="accessoire")
    supplier = models.ForeignKey(Supplier_m, on_delete=models.CASCADE, related_name='other', null=True, blank=True,
                                 default=None)

    def __str__(self):
        return f"Other - {self.name} / {self.supplier}"

    def get_absolute_url(self):
        return reverse("other_detail_n", kwargs={"id": self.id})

    def sh_price(self):
        return self.price

    def check_stock(self, quantity, *args):
        """checker la quantitée
            return True → tout va bien , on a assez de stock
            return x → il nous reste x unitées en stock
        """
        return True if int(self.stock) - int(quantity) >= 0 else int(self.stock)

    def sh_name(self):
        return f"{self.name}"

    def get_stock(self):
        return self.stock

    def reduce_stock(self, quantity):
        self.stock = self.stock - quantity

    def is_available(self):
        return self.supplier.is_available()

    def sh_supplier(self):
        return self.supplier.name

    def show_supplier_id(self):
        return self.supplier.id




class Pack_m(ImageConversionMixin, models.Model):
    """The model base for ant pack""" 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nest = models.ForeignKey(Other_m, on_delete=models.CASCADE, related_name='pack', null=True, default=None)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=20)
    size = models.OneToOneField(Size_m, null=True, on_delete=models.CASCADE)
    thumbnail_1 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_2 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_3 = models.ImageField(upload_to="products", null=True, blank=True)
    thumbnail_4 = models.ImageField(upload_to="products", null=True, blank=True)


    def __str__(self):
        return f"Pack - {self.size.product_base} - g{self.size.gyne} - w{self.size.worker} / {self.size.supplier}"

    def sh_name(self):
        return f"Pack {self.size.product_base.sh_name()}"

    def sh_price(self):
        return self.price

    def thumbnail_url(self):
        # Vérifier si thumbnail_1 a une image associée
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            # Si oui, retourner l'URL de thumbnail_1
            return self.thumbnail.url
        else:
            # Sinon, retourner l'URL de self.size.product_base.thumbnail
            return self.size.product_base.thumbnail.url

    def sh_spece(self):
        return self.size.product_base.spece

    def complete_spece(self):
        return self.size.product_base.under_spece

    def sh_localisation(self):
        return self.size.product_base.localisation

    def get_absolute_url(self):
        return reverse("pack_detail_n", kwargs={"id": self.id})

    def get_ant(self):
        return self.size.product_base

    def sh_description(self):
        return self.size.product_base.description

    def sh_description_complete(self):
        return f"Le pack contient le nid, la fondation, une pince à épiler, une seringue, un morceau de 10 cm de tuyau pour les liaisons \n {self.size.product_base.description} \n {self.nest.description}"

    def sh_problem(self):
        return bool(self.size.product_base.problem and self.problem)

    def check_stock(self, quantity, *args):
        """checker la quantitée
            return True → tout va bien , on a assez de stock
            return x → il nous reste x unitées en stock (de nid ou fondation)
        """
        if int(self.size.stock) - int(quantity) >= 0 and int(self.nest.stock) - (int(quantity) >= 0):
            return True
        else:
            if self.size.stock < self.nest.stock:
                st = self.size.stock
            elif self.nest.stock < self.size.stock:
                st = self.nest.stock
            elif self.nest.stock == self.size.stock:
                st = self.nest.stock

            return st

    def get_stock(self):
        if self.size.stock < self.nest.stock:
            st = self.size.stock
        elif self.nest.stock < self.size.stock or self.nest.stock == self.size.stock:
            st = self.nest.stock
        return st
        
    def reduce_stock(self, quantity):
        self.size.stock = self.size.stock - quantity

    def sh_supplier(self):
        return self.size.supplier.name

    def show_supplier_id(self):
        return self.size.supplier.id







