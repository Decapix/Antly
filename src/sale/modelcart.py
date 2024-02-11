import uuid
from django.db import models
from user.models import Shopper_m as Profile
from user.models import Address_m as Address
from .models import Ant_m, Pack_m, Other_m
from .extras import send_tracking_number_email, get_shipping_options
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.db.models import JSONField


# cart
from admin_supplier.models import Supplier_m


class OrderItem_m(models.Model):
    """for any product"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return '{0} - {1}'.format(self.content_type, self.owner)

    def sh_name(self):
        return self.content_object.sh_name()

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def get_stock(self):
        """return stock of the product"""
        if self.content_type != ContentType.objects.get_for_model(Ant_m):
            return int(self.content_object.get_stock())
        for y in self.content_object.get_sizes():
            if y.price == self.price:
                size = y
        return int(self.content_object.get_stock(size))


    def sh_type(self):
        other_m_ct = ContentType.objects.get_for_model(Other_m)
        pack_m_ct = ContentType.objects.get_for_model(Pack_m)
        ant_m_ct = ContentType.objects.get_for_model(Ant_m)

        if self.content_type == other_m_ct:
            return "other"
        elif self.content_type == pack_m_ct:
            return "pack"
        elif self.content_type == ant_m_ct:
            return "ant"


    def check_stock(self):
        """
        pour vérifier le stock des item de commande

        return True → tout va bien, il nous rest assez de stock
        return x → on a du reduire la quantitée de votre commande à x, on a plus assez
        return False → on a supprimée l'item de commande, notre stock est vide
        """
        # Obtenez le ContentType pour chaque modèle
        if self.content_type == ContentType.objects.get_for_model(Ant_m):
            for y in self.content_object.get_sizes():
                if y.price == self.price:
                    size = y
            result = self.content_object.check_stock(self.quantity, size)
            match result:
                case True:
                    return True
                case _:
                    if type(result) == int:
                        if result - self.quantity >= 0:
                            self.quantity = result - self.quantity
                            self.save()
                            return self.quantity
                        else:
                            self.delete()
                            return False
        else:
            result = self.content_object.check_stock(self.quantity)
            match result:
                case True:
                    return True
                case _:
                    if type(result) == int:
                        if result - self.quantity >= 0:
                            self.quantity = result - self.quantity
                            self.save()
                            return self.quantity
                        else:
                            self.delete()
                            return False
    

    def reduce_stock(self):
        """
        pour réduire le stock des produits apres la commande
        """
        # Obtenez le ContentType pour chaque modèle
        if self.content_type == ContentType.objects.get_for_model(Ant_m):
            for y in self.content_object.get_sizes():
                if y.price == self.price:
                    size = y
                    size.stock = size.stock - self.quantity

        else:
            self.content_object.reduce_stock(self.quantity)


    def sh_titlecart(self):
        # Obtenez le ContentType pour chaque modèle
        other_m_ct = ContentType.objects.get_for_model(Other_m)
        pack_m_ct = ContentType.objects.get_for_model(Pack_m)
        ant_m_ct = ContentType.objects.get_for_model(Ant_m)

        # Utilisez une structure conditionnelle classique pour effectuer les vérifications
        if self.content_type == other_m_ct:
            return f"{self.content_object.type} - {self.content_object.name}"
        elif self.content_type == pack_m_ct:
            return f"{self.content_object.size.gyne} gyne - {self.content_object.size.worker} ouvrières"
        elif self.content_type == ant_m_ct:
            for y in self.content_object.get_sizes():
                if y.price == self.price:
                    size = y
            return f"{size.gyne} gyne - {size.worker} ouvrières"

    def sh_supplier(self):
        """name of supplier"""
        # Obtenez le ContentType pour chaque modèle
        other_m_ct = ContentType.objects.get_for_model(Other_m)
        pack_m_ct = ContentType.objects.get_for_model(Pack_m)
        ant_m_ct = ContentType.objects.get_for_model(Ant_m)

        # Utilisez une structure conditionnelle classique pour effectuer les vérifications
        if self.content_type == other_m_ct or self.content_type != pack_m_ct and self.content_type == ant_m_ct:
            return self.content_object.sh_supplier()
        elif self.content_type == pack_m_ct:
            return self.content_object.size.sh_supplier()

    def show_supplier_id(self):
        """id of supplier"""
        # Obtenez le ContentType pour chaque modèle
        other_m_ct = ContentType.objects.get_for_model(Other_m)
        pack_m_ct = ContentType.objects.get_for_model(Pack_m)
        ant_m_ct = ContentType.objects.get_for_model(Ant_m)

        # Utilisez une structure conditionnelle classique pour effectuer les vérifications
        if self.content_type == other_m_ct or self.content_type != pack_m_ct and self.content_type == ant_m_ct:
            return self.content_object.show_supplier_id()
        elif self.content_type == pack_m_ct:
            return self.content_object.size.show_supplier_id()



class Order_m(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=15, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem_m)
    date_ordered = models.DateTimeField(auto_now=True)
    address = models.OneToOneField(Address, null=True, on_delete=models.SET_NULL)
    delivery_option = JSONField(null=True, blank=True)    

    def shipping_costs(self):
        if settings.FREE_SHIPPING_COSTE:
            return 0
        else:
            total_cost = 0

            # Vérification si delivery_option est vide ou None
            if not self.delivery_option or not isinstance(self.delivery_option, dict):
                return total_cost

            # Parcourir les options de livraison pour chaque fournisseur
            for supplier_id, shipping_options in self.delivery_option.items():
                if not shipping_options or not isinstance(shipping_options, list):
                    continue  # Ignore si les options de livraison ne sont pas une liste valide

                # Extraire les prix des options de livraison et les convertir en float
                try:
                    prices = [float(option.split(' - ')[1]) for option in shipping_options if ' - ' in option]
                except ValueError:
                    continue  # Ignore si les prix ne peuvent pas être convertis en float

                # Ajouter le prix le moins cher au coût total
                if prices:
                    total_cost += min(prices)

            return total_cost

    
    def set_delivery_methode(self):
        # all items 
        ele= []
        for i in self.items.all() :
            ele.append(i)
        # remove duplicate
        elenv = []
        for element in ele:
            if element not in elenv:
                elenv.append(element)
        ele = elenv
        # get seller 
        seller = []
        for element in ele:
            seller.append(element.show_supplier_id())
        # country 
        country = []
        for i in seller :
            supplier = Supplier_m.objects.get(id=i)
            terr = supplier.country
            country.append((supplier, terr))
        
        # Code du pays de destination
        to_country_code = self.address.country

        # Dictionnaire pour stocker les options de livraison pour chaque fournisseur
        delivery_options_per_supplier = {}

        # Parcourir chaque couple fournisseur-destination
        for supplier, from_country_code in country:
            # Obtenir les options de livraison pour le couple fournisseur-destination
            shipping_options = get_shipping_options(from_country_code.code, to_country_code)

            # Convertir la liste des options en format lisible
            shipping_options_list = [f"{service} - {price}" for service, price in shipping_options]

            # Convertir supplier.id en chaîne de caractères
            supplier_id_str = str(supplier.id)

            # Ajouter les options de livraison pour ce fournisseur
            delivery_options_per_supplier[supplier_id_str] = shipping_options_list

        # Enregistrer les options de livraison dans le champ JSON
        self.delivery_option = delivery_options_per_supplier
        self.save()


        
    
    def gift(self):
        if settings.FREE_COLONIE:
            n = sum(item.quantity for item in self.items.all() if item.is_ordered == False)
            if n >= 3:
                return True
        elif settings.FREE_COLONIE2:
            n = sum(item.quantity for item in self.items.all() if item.is_ordered == False)
            if n >= 2:
                return True
        elif settings.FREE_COLONIE1:
            n = sum(item.quantity for item in self.items.all() if item.is_ordered == False)
            if n >= 1:
                return True
        return False


    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        """total + shippings price
        befor is ordered"""
        return int(self.shipping_costs()) + sum(
            item.quantity * item.price for item in self.items.all() if item.is_ordered == False)

    def get_cart_price(self):
        """total
                befor is ordered"""
        return int(sum(item.quantity * item.price for item in self.items.all() if item.is_ordered == False))

    def get_order_total(self):
        """total + shippings price
                after is ordered"""
        return int(self.shipping_costs()) + sum(
            item.quantity * item.price for item in self.items.all() if item.is_ordered == True)

    def __str__(self):
        if self.is_ordered :
            return '{0} - {1} - {2}'.format(self.owner, self.date_ordered,  self.ref_code)
        return '{0} - {1}'.format(self.owner, self.ref_code)

    def check_stock(self):
        """return list with items"""
        it = []
        for i in self.items.all():
            i.check_stock()
            it.append(i)
        return it

    def get_item_supplier(self, supplier_id):
        ele= []
        for i in self.get_cart_items() :
            if i.show_supplier_id == supplier_id:
                ele.append(i)
        return ele
    

    
    def shipping_cost_reasons(self):
        reasons_html = ""

        if not self.delivery_option or not isinstance(self.delivery_option, dict):
            return reasons_html

        for supplier_id, shipping_options in self.delivery_option.items():
            # Convertir l'UUID en string si nécessaire
            supplier_id_str = str(supplier_id)

            # Récupérer le fournisseur
            supplier = Supplier_m.objects.get(id=supplier_id_str)

            # Récupérer les articles associés au fournisseur
            supplier_items = [item for item in self.items.all() if str(item.show_supplier_id()) == supplier_id_str]

            # Construire une liste des noms des articles
            item_names = [item.sh_name() for item in supplier_items]

            if shipping_options:
                # Trouver l'option la moins chère et son prix
                cheapest_option, cheapest_price = min((opt.split(' - ') for opt in shipping_options), key=lambda x: float(x[1]))
                country_from = supplier.country.name

                # Ajouter au HTML, incluant le prix
                reasons_html += _("<p>Le colis de <b>{supplier_name}</b> part de <b>{country}</b> avec <b>{service}</b> pour <b>{price}€</b>, il contient {items}.</p>").format(
                    supplier_name=supplier.name, country=country_from, service=cheapest_option, price=cheapest_price, items=", ".join(item_names))

        return reasons_html
    





class OrderTrack_m (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_track = models.CharField(max_length=30, null=True, blank=True)
    order = models.ForeignKey(Order_m, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"order {self.order} - {self.order_track}"


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





    