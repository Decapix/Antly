import re
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
import stripe
from sale.models import Product_m as Product
from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from admin_supplier.models import Supplier_m
from sale.models import Ant_m, Other_m, Pack_m


def sup(value):
    """just for remove the end of an email """
    value = str(value)
    va = ""
    for i in value:
        if i == "@":
            return va.replace('.', ' ')
        else:
            va = va + i


def num_format(chaine):
    chaine = chaine.replace(" ", "")
    pattern = re.compile(r'^(?:\+33|33)?\(?(?:0)?\)?[1-9](?:[\.\-]?[0-9]{2}){4}$')
    match = pattern.match(chaine)

    if not match:
        raise ValueError("Le numéro de téléphone n'est pas valide.")

    # Supprimer le préfixe international et le préfixe national
    numero = re.sub(r'^(\+33|33)?\(?(0)?\)?', '', chaine)

    # Formatter le numéro en utilisant des espaces
    numero_formate = ''.join([numero[i:i + 2] for i in range(0, len(numero), 2)])

    return f"0{numero_formate}"


def validate_phone_number(value):
    try:
        num_format(value)
    except ValueError:
        raise ValidationError("Le numéro de téléphone n'est pas valide.")


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Shopper_m(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(('email address'), unique=True)

    username = models.CharField(
        ("username"),
        max_length=150,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
        null = True, blank = True
    )

    why_ant = models.CharField(max_length=2000, null=True, blank=True)
    favorite_specie = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()



    def user_name(self):
        if self.username:
            return self.username
        else:
            return sup(self.email)

    def __str__(self):
        return self.user_name()



    
    # payment methods


# def post_save_profile_create(sender, instance, created, *args, **kwargs):
#     user_profile, created = Shopper_m.objects.get_or_create(user=instance)
#
#     if user_profile.stripe_id is None or user_profile.stripe_id == '':
#         new_stripe_id = stripe.Customer.create(email=instance.email)
#         user_profile.stripe_id = new_stripe_id['id']
#         user_profile.save()
#
#
# post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)





class Address_m(models.Model):
    country = models.CharField(max_length=100)
    complete_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30, validators=[validate_phone_number])
    adress = models.CharField(max_length=300)
    detail = models.CharField(max_length=300, blank=True, null=True)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"address - {self.complete_name}"


class Feedback_m(models.Model):
    text = models.CharField(max_length=2000)
    star = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="La note doit être supérieure ou égale à 1."),
            MaxValueValidator(5, message="La note doit être inférieure ou égale à 5.")
        ], help_text="Veuillez attribuer une note entre 1 et 5.",
    )
    shopper = models.ForeignKey(Shopper_m, on_delete=models.CASCADE, null=True, blank=True)

    supplier =  models.ForeignKey(Supplier_m, on_delete=models.SET_NULL , null=True, blank=True)
    antly = models.BooleanField(default=False)
    product_ant = models.ForeignKey(Ant_m, on_delete=models.SET_NULL , null=True, blank=True)
    product_other = models.ForeignKey(Other_m, on_delete=models.SET_NULL, null=True, blank=True)
    product_pack = models.ForeignKey(Pack_m, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"feedback - {self.shopper} - {self.star}/5"

    def sh_subject(self):
        subjects = []

        # Vérifiez si le commentaire est lié à un fournisseur
        if self.supplier:
            subjects.append(f"{self.supplier.name} (vendeur)")

        # Vérifiez si le commentaire est lié à antly
        if self.antly:
            subjects.append("Antly")

        # Vérifiez si le commentaire est lié à un produit de type ant
        if self.product_ant:
            subjects.append(str(self.product_ant.sh_name()))

        # Vérifiez si le commentaire est lié à un autre type de produit
        if self.product_other:
            subjects.append(str(self.product_other.sh_name()))

        # Vérifiez si le commentaire est lié à un pack de produits
        if self.product_pack:
            subjects.append(str(self.product_pack.sh_name()))

        # Retournez la liste des sujets sous forme de chaîne, séparée par des virgules
        return ", ".join(subjects)



