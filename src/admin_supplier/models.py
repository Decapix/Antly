import uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

COUNTRY_CHOICES = (
    ("Algérie", "Algeria"),
    ("Australie", "Australia"),
    ("Bangladesh", "Bangladesh"),
    ("Belgique", "Belgium"),
    ("Bhoutan", "Bhutan"),
    ("Brunei", "Brunei"),
    ("Burundi", "Burundi"),
    ("Cambodge", "Cambodia"),
    ("Chine", "China"),
    ("Comores", "Comoros"),
    ("Corée", "Korea"),
    ("Corse", "Corsica"),
    ("Côte d'Ivoire", "Ivory Coast"),
    ("Espagne", "Spain"),
    ("Émirats Arabes Unis", "United Arab Emirates"),
    ("Égypte", "Egypt"),
    ("Éthiopie", "Ethiopia"),
    ("France", "France"),
    ("Gambie", "Gambia"),
    ("Ghana", "Ghana"),
    ("Grèce", "Greece"),
    ("Inde", "India"),
    ("Indonésie", "Indonesia"),
    ("Iran", "Iran"),
    ("Irak", "Iraq"),
    ("Irlande", "Ireland"),
    ("Israël", "Israel"),
    ("Italie", "Italy"),
    ("Japon", "Japan"),
    ("Jordanie", "Jordan"),
    ("Kazakhstan", "Kazakhstan"),
    ("Kenya", "Kenya"),
    ("Laos", "Laos"),
    ("Liban", "Lebanon"),
    ("Liberia", "Liberia"),
    ("Libye", "Libya"),
    ("Luxembourg", "Luxembourg"),
    ("Madagascar", "Madagascar"),
    ("Malaisie", "Malaysia"),
    ("Maroc", "Morocco"),
    ("Mauritanie", "Mauritania"),
    ("Méditerranée", "Mediterranean"),
    ("Mongolie", "Mongolia"),
    ("Mozambique", "Mozambique"),
    ("Myanmar", "Myanmar"),
    ("Népal", "Nepal"),
    ("Nigeria", "Nigeria"),
    ("Nord de la France", "North France"),
    ("Nouvelle-Zélande", "New Zealand"),
    ("Océan Indien", "Indian Ocean"),
    ("Oman", "Oman"),
    ("Pakistan", "Pakistan"),
    ("Papouasie-Nouvelle-Guinée", "Papua New Guinea"),
    ("Philippines", "Philippines"),
    ("Polynésie française", "French Polynesia"),
    ("Portugal", "Portugal"),
    ("Qatar", "Qatar"),
    ("Russie", "Russia"),
    ("Rwanda", "Rwanda"),
    ("Samoa", "Samoa"),
    ("Scandinavie", "Scandinavia"),
    ("Sénégal", "Senegal"),
    ("Seychelles", "Seychelles"),
    ("Sicile", "Sicily"),
    ("Sierra Leone", "Sierra Leone"),
    ("Singapour", "Singapore"),
    ("Soudan", "Sudan"),
    ("Sri Lanka", "Sri Lanka"),
    ("Sud de la France", "South France"),
    ("Suisse", "Switzerland"),
    ("Syrie", "Syria"),
    ("Tadjikistan", "Tajikistan"),
    ("Tanzanie", "Tanzania"),
    ("Thaïlande", "Thailand"),
    ("Timor Oriental", "East Timor"),
    ("Togo", "Togo"),
    ("Tunisie", "Tunisia"),
    ("Turkménistan", "Turkmenistan"),
    ("Turquie", "Turkey"),
    ("Ukraine", "Ukraine"),
    ("Uruguay", "Uruguay"),
    ("Vanuatu", "Vanuatu"),
)

class Supplier_m(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    currently_available = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to="products", null=True, blank=True)
    description = models.TextField(max_length=3000,  null=True, blank=True)
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES, default="1")

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.id)

    def is_available(self):
        return self.currently_available

    def thumbnail_url(self):
        return self.thumbnail.url








