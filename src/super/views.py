import random
from django.shortcuts import render
from sale.models import *
from user.models import Feedback_m
from .models import *
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

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
    offers = Offer_m.objects.filter(active=True)
    return render(request, 'super/information.html', context={"meta": metat, "offers": offers})


def cgv_vi(request):
    """view for cgv"""
    metat = MetaTemplate(
        "Conditions Générales de Vente | Boutique en Ligne de Fourmis Européennes pour Débutants",
        "Consultez les conditions générales de vente de notre boutique en ligne de fourmis européennes pour débutants. Découvrez nos politiques concernant les commandes, les prix, les paiements, les livraisons, les retours et la responsabilité, ainsi que des informations sur les données personnelles et le service clientèle.")
    return render(request, 'super/cgv.html', context={"meta": metat,})



@require_GET
@csrf_exempt
def superfeed_xml_view(request):
    # Retrieve all Ant_m, Pack_m, and Other_m products
    ant_products = Ant_m.objects.filter(sizes__stock__gt=0).distinct()
    pack_products = Pack_m.objects.filter(size__stock__gt=0).distinct()
    #other_products = Other_m.objects.filter(stock__gt=0).distinct()

    # Load the template for the superfeed.xml file
    template = loader.get_template('super/superfeed.xml')

    # Context data to be passed to the template
    context = {
        'ant_products': ant_products,
        'pack_products': pack_products,
   #     'other_products': other_products,
    }

    # Render the template with the context data
    rendered_template = template.render(context)

    # Set the appropriate content type for the XML response
    response = HttpResponse(content_type='application/xml')

    # Set the content of the response to the rendered template
    response.content = rendered_template

    return response