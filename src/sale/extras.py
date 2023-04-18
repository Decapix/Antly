from django.conf import settings
import random
import string
from datetime import date
import datetime



def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for _ in range(3)])
    return date_str + rand_str





def offer_ant_func(ant_product, l1, l2):
    ant = l1 + l2
    offer_ant1 = []
    offer_ant2 = []
    offer_ant3 = []
    offer_ant4 = []
    # algo for offer ant, end page
    for antt in ant:
        if antt.spece == ant_product.spece:
            if antt.localisation == ant_product.localisation:
                offer_ant1.append(antt)
            else:
                offer_ant2.append(antt)
        elif antt.localisation == ant_product.localisation:
            offer_ant3.append(antt)
        else:
            offer_ant4.append(antt)
    offer_ant = offer_ant1 + offer_ant2 + offer_ant3 + offer_ant4
    for i in offer_ant:
        if i.id == ant_product.id:
            offer_ant.remove(i)
    return offer_ant[:6] if len(offer_ant) > 6 else offer_ant




