import random
from django.shortcuts import render
from sale.models import *
from user.models import Feedback_m
from .models import *


def random_three_elements(input_list):
    if len(input_list) < 3:
        raise ValueError("La liste doit contenir au moins trois éléments.")

    return random.sample(input_list, 3)

def homepage_vi(request):
    """view for homepage"""
    metat = MetaTemplate("Boutique en Ligne de Fourmis pour Débutants - Fondations, Packs, Nids et Accessoires | Myrmécologie",
                         "Bienvenue sur notre boutique en ligne de fourmis pour débutants ! Découvrez notre sélection de fondations, packs, nids et accessoires pour commencer votre élevage de fourmis. Profitez de conseils d'experts et rejoignez la communauté des passionnés de Myrmécologie.")
    ant = Ant_m.objects.filter(sizes__stock__gt=0).distinct()
    pack = Pack_m.objects.filter(size__stock__gt=0).distinct()
    comment = Feedback_m.objects.all()
    if len(comment) >= 3:
        comment = random_three_elements(list(comment))
    product = list(ant) + list(pack)
    # offer
    offers = None
    if not request.session.get('offer_shown', False):
        offers = Offer_m.objects.filter(active=True)
        request.session['offer_shown'] = True
        request.session.modified = True
    return render(request, 'super/homepage.html', context={"product": product, "meta": metat, "comment": comment, "offers": offers})





def information_vi(request):
    """view for information"""
    metat = MetaTemplate(
        "Informations | Boutique en Ligne de Fourmis Européennes pour Débutants",
        "Découvrez toutes les informations importantes concernant notre boutique en ligne de fourmis européennes pour débutants. Informez-vous sur nos options de livraison, modes de paiement, conditions d'utilisation, politique de confidentialité, mentions légales, expédition et retours, qui nous sommes, cookies et comment nous contacter.")
    return render(request, 'super/information.html', context={"meta": metat})


def cgv_vi(request):
    """view for cgv"""
    metat = MetaTemplate(
        "Conditions Générales de Vente | Boutique en Ligne de Fourmis Européennes pour Débutants",
        "Consultez les conditions générales de vente de notre boutique en ligne de fourmis européennes pour débutants. Découvrez nos politiques concernant les commandes, les prix, les paiements, les livraisons, les retours et la responsabilité, ainsi que des informations sur les données personnelles et le service clientèle.")
    return render(request, 'super/cgv.html', context={"meta": metat,})