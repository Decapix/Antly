import random
import string
from datetime import date
import datetime
from django.template.loader import render_to_string
from django.contrib import messages
from .extras import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Supplier_m, Ant_m, Other_m, Pack_m
import requests
import json




def send_tracking_number_email(order, latest_order_track):
    mail_subject = "Antly - Expédition de votre commande et numéro de suivi"
    current_date = timezone.now()
    new_date = current_date + timedelta(days=3)


    context = {
        'user': order.owner,
        'order': order,
        'tracking_number': latest_order_track.order_track if latest_order_track else None,
        'shipping_date': current_date,  # À remplacer par la date d'expédition si différente
        'estimated_delivery_date': new_date,  # À remplacer par la date estimée de livraison
        'carrier_name': 'Colissimo',  # À remplacer par le nom du transporteur
        'tracking_url': 'https://www.laposte.fr/outils/track-a-parcel',  # À remplacer par l'URL de suivi du colis
        'customer_service_email': 'antly.fourmis@gmail.com',
    }

    message = render_to_string('sale/tracking_email_template.txt', context)

    email = EmailMessage(mail_subject, message, to=[order.owner.email] )
    email.send()
    


def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for _ in range(3)])
    return date_str + rand_str



def offer_ant_func(ant_product, l1, l2, l3):
    ant = l1 + l2
    offer_ant1 = []
    offer_ant2 = []
    offer_ant3 = []
    offer_ant4 = []
    # algo for offer ant, end page
    for antt in ant:
        if antt.sh_spece() == ant_product.sh_spece():
            if antt.sh_localisation() == ant_product.sh_localisation():
                offer_ant1.append(antt)
            else:
                offer_ant2.append(antt)
        elif antt.sh_localisation() == ant_product.sh_localisation():
            offer_ant3.append(antt)
        else:
            offer_ant4.append(antt)
    offer_ant = offer_ant1 + offer_ant2 + offer_ant3 + offer_ant4
    for i in offer_ant:
        if i.id == ant_product.id:
            offer_ant.remove(i)
    # reduce to 5
    offer_ant = offer_ant[:5] if len(offer_ant) > 5 else offer_ant
    # get other product
    if l3:
        other = random.choice(l3)
        position = random.randint(0, len(offer_ant))
        # add other to the list
        offer_ant.insert(position, other)
    return offer_ant


def offer_other_func(other_product, l1, l2, l3):
    list_product = l1 + l2 + l3
    for i in list_product:
        if i.id == other_product.id:
            list_product.remove(i)
    if len(list_product) <= 6:
        return list_product
    list_product = random.sample(list_product, 6)
    return list_product





def get_products_for_supplier(supplier_id):
    # Récupérer l'instance du fournisseur
    supplier = Supplier_m.objects.get(id=supplier_id)

    # Récupérer les produits 'ant' associés
    ants = Ant_m.objects.filter(supplier=supplier)

    # Récupérer les produits 'other' associés
    others = Other_m.objects.filter(supplier=supplier)

    # Récupérer les produits 'pack' associés
    # Pour éviter l'importation circulaire, utilisez l'identifiant du fournisseur directement
    packs = Pack_m.objects.filter(size__supplier=supplier)

    product = list(ants) + list(packs) + list(others)

    return product



def calculer_frais_envoi(adresse_acheteur, adresse_vendeur, poids, dimensions):
    url = "https://onlinetools.ups.com/ship/v1/rating/Rate"
    headers = {
        "Content-Type": "application/json",
        "Username": "VOTRE_NOM_UTILISATEUR_UPS",
        "Password": "VOTRE_MOT_DE_PASSE_UPS",
        "AccessLicenseNumber": "VOTRE_CLE_ACCESS_UPS"
    }

    # Construire la requête en suivant la structure attendue par l'API UPS
    # Notez que cette structure doit être adaptée en fonction de vos besoins spécifiques et des données disponibles
    body = {
        "RateRequest": {
            "Shipment": {
                "Shipper": {
                    "Address": {
                        "PostalCode": adresse_vendeur['code_postal'],
                        "CountryCode": adresse_vendeur['pays']
                    }
                },
                "ShipTo": {
                    "Address": {
                        "PostalCode": adresse_acheteur['code_postal'],
                        "CountryCode": adresse_acheteur['pays']
                    }
                },
                "ShipFrom": {
                    "Address": {
                        "PostalCode": adresse_vendeur['code_postal'],
                        "CountryCode": adresse_vendeur['pays']
                    }
                },
                "Package": {
                    "PackagingType": {
                        "Code": "02"
                    },
                    "Dimensions": dimensions,
                    "PackageWeight": {
                        "UnitOfMeasurement": {
                            "Code": "KGS"
                        },
                        "Weight": poids
                    }
                }
            }
        }
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None



def easypostcalcul ():

    client = easypost.EasyPostClient(settings.EASYPOST_API_TEST)
    print("clienttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt", client)

    shipment_details = {
    "to_address": {
        "name": "Dr. Steve Brule",
        "street1": "179 N Harbor Dr",
        "city": "Redondo Beach",
        "state": "CA",
        "zip": "90277",
        "country": "US",
        "phone": "4153334444",
        "email": "dr_steve_brule@gmail.com",
    },
    "from_address": {
        "name": "EasyPost",
        "street1": "417 Montgomery Street",
        "street2": "5th Floor",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94104",
        "country": "US",
        "phone": "4153334444",
        "email": "support@easypost.com",
    },
    "parcel": {
        "length": 20.2,
        "width": 10.9,
        "height": 5,
        "weight": 65.9,
    },
    }

    rates = client.beta_rate.retrieve_stateless_rates(**shipment_details)

    print("rates", rates)