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





