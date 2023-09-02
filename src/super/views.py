import random
from django.contrib import messages
from django.shortcuts import render
from sale.models import *
from user.models import Feedback_m
from .models import *
from .classifications import ant_species
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .breadcrumbs import *


def random_three_elements(input_list):
    if len(input_list) < 3:
        raise ValueError("La liste doit contenir au moins trois éléments.")

    return random.sample(input_list, 3)

def homepage_vi(request):
    """view for homepage"""
    metat = MetaTemplate("Boutique en Ligne de Fourmis pour Débutants - Fondations, Packs, Nids et Accessoires | Myrmécologie",
                         "Bienvenue sur notre boutique en ligne de fourmis pour débutants ! Découvrez notre sélection de fondations, packs, nids et accessoires pour commencer votre élevage de fourmis. Profitez de conseils d'experts et rejoignez la communauté des passionnés de Myrmécologie.")
    bread = [pageAccueil]
    ant = Ant_m.objects.filter(sizes__stock__gt=0, supplier__currently_available = True, problem=False).distinct()
    pack = Pack_m.objects.filter(size__stock__gt=0, supplier__currently_available = True, nest__problem=False).distinct()
    other = Other_m.objects.filter(stock__gt=0, supplier__currently_available = True, problem=False).distinct()
    comment = Feedback_m.objects.all()
    if len(comment) >= 3:
        comment = random_three_elements(list(comment))
    product = list(ant) + list(pack) + list(other)
    if len(product) > 20:
        product = product[:20]
    # offer
    offers = None
    if not request.session.get('offer_shown', False):
        offers = Offer_m.objects.filter(active=True)
        request.session['offer_shown'] = True
        request.session.modified = True
    return render(request, 'super/homepage.html', context={"product": product, "meta": metat, "comment": comment, "offers": offers, "bread": bread})





def information_vi(request):
    """view for information"""
    bread = [pageAccueil, pageInformation]
    metat = MetaTemplate(
        "Informations | Boutique en Ligne de Fourmis Européennes pour Débutants",
        "Découvrez toutes les informations importantes concernant notre boutique en ligne de fourmis européennes pour débutants. Informez-vous sur nos options de livraison, modes de paiement, conditions d'utilisation, politique de confidentialité, mentions légales, expédition et retours, qui nous sommes, cookies et comment nous contacter.")
    offers = Offer_m.objects.filter(active=True)
    return render(request, 'super/information.html', context={"meta": metat, "offers": offers, "bread": bread})


def cgv_vi(request):
    """view for cgv"""
    bread = [pageAccueil, pageInformation, pageCvg]
    metat = MetaTemplate(
        "Conditions Générales de Vente | Boutique en Ligne de Fourmis Européennes pour Débutants",
        "Consultez les conditions générales de vente de notre boutique en ligne de fourmis européennes pour débutants. Découvrez nos politiques concernant les commandes, les prix, les paiements, les livraisons, les retours et la responsabilité, ainsi que des informations sur les données personnelles et le service clientèle.")
    return render(request, 'super/cgv.html', context={"meta": metat, "bread": bread})



@require_GET
@csrf_exempt
def superfeed_xml_view(request):
    # Retrieve all Ant_m, Pack_m, and Other_m products
    ant_products = Ant_m.objects.filter(sizes__stock__gt=0).distinct()
    pack_products = Pack_m.objects.filter(size__stock__gt=0).distinct()
    other_products = Other_m.objects.filter(stock__gt=0).distinct()

    # Load the template for the superfeed.xml file
    template = loader.get_template('super/superfeed.xml')

    # Context data to be passed to the template
    context = {
        'ant_products': ant_products,
        'pack_products': pack_products,
        'other_products': other_products,
    }

    # Render the template with the context data
    rendered_template = template.render(context)

    # Set the appropriate content type for the XML response
    response = HttpResponse(content_type='application/xml')

    # Set the content of the response to the rendered template
    response.content = rendered_template

    return response


def specie_form(request):
    """view for the form specie"""
    metat = MetaTemplate(
        "Élevage de Fourmis - Guide Complet pour Débutants et Experts | Antly",
        "Explorez le monde de l'élevage de fourmis avec Antly. Que vous soyez débutant ou expert, trouvez l'espèce " 
        "idéale pour vous grâce à notre guide interactif. Commencez votre aventure avec nos fourmis aujourd'hui !", )

    bread = [pageAccueil, pageChoisir]

    if request.method == "POST":
        level = request.POST.get("niveau", default="debutant")
        taille = request.POST.get("taille", default="none")
        couleur = request.POST.get("couleur",  default="none")
        localisations = request.POST.getlist('localisation')

        activite = request.POST.get("activite", default="none")
        nid = request.POST.get("nid", default="none")
        # traitement

        # fourmis qui pourrait corespondre
        su = {}
        match level:
            case "debutant":
                su["z_level"] = 1
            case "intermediaire":
                su["z_level"] = 2
            case "experimente":
                su["z_level"]= 3

        su["z_region"] = []
        if "sans importance" in localisations:
            su["z_region"] = None
        else:
            for localisation in localisations:
                match localisation:
                    case "Europe du Sud":
                        su["z_region"].append("Southern-Europe")
                    case "Europe du Nord":
                        su["z_region"].append("Northern-Europe")
                    case "Asie":
                        su["z_region"].append("Asia")
                    case "Amérique du Sud":
                        su["z_region"].append("South-America")
                    case "Amérique du Nord":
                        su["z_region"].append("North-America")
                    case "Australie":
                        su["z_region"].append("Australia")
                    case "Afrique":
                        su["z_region"].append("Africa")


        match taille :
            case "true" :
                su["z_taille"] = True
            case "false":
                su["z_taille"] = False
            case "none":
                su["z_taille"] = None

        match couleur:
            case "true":
                su["z_couleur"] = True
            case "false":
                su["z_couleur"] = False
            case "none":
                su["z_couleur"] = None


        match activite:
            case "true":
                su["z_activite"] = True
            case "false":
                su["z_activite"] = False
            case "none":
                su["z_activite"] = None

        match nid:
            case "true":
                su["z_nid"] = True
            case "false":
                su["z_nid"] = False
            case "none":
                su["z_nid"] = None

        def filter_ant_species(ant_species, su):
            filtered_ant_species = [species for species in ant_species if
                                    (species['breeding_level'] <= su['z_level']) and
                                    (su['z_region'] is None or species['Region'] in su['z_region']) and
                                    (su['z_taille'] is None or species['Size'] == su['z_taille']) and
                                    (su['z_couleur'] is None or species['Color'] == su['z_couleur']) and
                                    (su['z_activite'] is None or species['Activity'] == su['z_activite']) and
                                    (su['z_nid'] is None or species['Nest'] == su['z_nid'])]
            return filtered_ant_species

        # Utilisez la fonction pour filtrer les espèces d'ant
        filtered_species = filter_ant_species(ant_species, su)
        if len(filtered_species) == 0 :
            speci = "<p>Désolé, nous n'avons pas trouvé d'espèces correspondant à vos critères, toutefois ne perdez pas" \
                    " espoire, voici une liste contenant toutes les espèces réferencées à ce jour, vous trouverez bien votre bonheurs !</p>" \
                    "<a href='https://www.antwiki.org/wiki/Category:Extant_species'>espèces</a>"

            txt_dispo = "none"

        else :
            speci = "<p>" + ", ".join([i["Specie"] for i in filtered_species]) + "</p>"

            # check ant in stock

            def process_string(input_string):
                return input_string.replace(" ", "").lower()

            ant_stock = Ant_m.objects.filter(sizes__stock__gt=0).distinct()

            def filter_stock(filtered_species, ant_stock):
                dispo = []
                for i in ant_stock:
                    dispo.extend(i for o in filtered_species if process_string(o["Specie"]) == process_string(i.sh_name()))

                return dispo

            dispo = filter_stock(filtered_species, ant_stock)
            if len(dispo) == 0 :
                txt_dispo = "none"
            else :
                txt_dispo = """
                        <div class="row">
                        """
                for p in dispo:
                    txt_dispo += f"""
                            <div class="col-md-4">
                                <div class="card border-0 mb-4">
                                    <a class= "exemple" href="{p.get_absolute_url()}">
                                        <img src="{p.thumbnail_url()}" alt="" class="card-img-top w-100 limite-height">
                                        <div class="card-body">
                                            <h6 class="card-title">{p.sh_name()}</h6>
                                            <p>{p.sh_price()} €</p>
                                        </div>
                                    </a>
                                </div>
                            </div>
                            """
                txt_dispo += "</div>"

        address_json = {
            "specie": speci,
            "stock": txt_dispo,
        }

        return JsonResponse(address_json)
    return render(request, 'super/specie_form.html', context={"meta": metat,  "bread": bread})