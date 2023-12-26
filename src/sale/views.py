from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from .forms import UpdateQuantityForm
from .models import *
from .modelcart import *
from django.utils import timezone
import stripe
from user.models import Shopper_m as Profile
from user.models import Address_m
from user.forms import Address_fo
from django.contrib import messages
from .extras import *
from django.core.mail import EmailMessage
from super.models import MetaTemplate
from django.views import View
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
import os
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.templatetags.static import static as stat
from django.contrib.staticfiles import finders
from django.contrib.contenttypes.models import ContentType
from super.breadcrumbs import *
from admin_supplier.models import Supplier_m
from user.models import Feedback_m
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm




def get_user_pending_order(request):
    """
    Get the pending order for the given user.

    Args:
        request: The user's request object.

    Returns:
        The pending order object if it exists, otherwise 0.
    """
    user_profile = request.user
    order = Order_m.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # Get the first (and only) order in the filtered orders list
        return order[0]
    return 0


def ant_product_vi(request):
    """
    Render the ant product view.

    Args:
        request: The user's request object.

    Returns:
        The rendered ant product view with context data.
    """
    metat = MetaTemplate(
        "Fondations de Fourmis pour Débutants - Achat et Vente de Colonies de Fourmis | Boutique en Ligne",
        "Explorez notre collection de fondations de fourmis pour débutants, avec une variété d'espèces et d'origines. Démarrez votre élevage de fourmis en toute simplicité et bénéficiez d'un support professionnel. Découvrez nos offres dès maintenant !")

    bread = [pageAccueil, pageFourmis]
    ant_product = Ant_m.objects.filter(sizes__stock__gt=0, supplier__currently_available = True).distinct()
    country = []
    for ant in ant_product:
        if ant.sh_localisation() not in country:
            country.append(ant.sh_localisation())
    return render(request, 'sale/ant_product.html', context={"ant_product": ant_product, "country": country, 'meta':metat, "bread": bread})


def other_product_vi(request):
    """
    Render the ant product view.

    Args:
        request: The user's request object.

    Returns:
        The rendered ant product view with context data.
    """
    metat = MetaTemplate(
        "Accessoires pour l'élevage de Fourmis - Nids, Outils et Plus | Boutique en Ligne",
"Découvrez notre gamme complète d'accessoires pour l'élevage de fourmis, conçue pour les débutants. De la mise en place de votre nid à la maintenance de votre colonie, nos produits assurent une expérience optimale. Visitez notre boutique et découvrez nos offres !")
    bread = [pageAccueil, pageOther]
    other_product = Other_m.objects.filter(stock__gt=0, supplier__currently_available = True).distinct()
    country = []
    for ant in other_product:
        if ant.type not in country:
            country.append(ant.type)
    return render(request, 'sale/other_product.html', context={"other_product": other_product, "country": country, 'meta':metat, "bread":bread})


def pack_product_vi(request):
    """
    Render the pack product view.

    Args:
        request: The user's request object.

    Returns:
        The rendered pack product view with context data.
    """
    metat = MetaTemplate(
        "Packs pour Élevage de Fourmis Débutants - Achat et Vente de Packs Fourmis | Boutique en Ligne",
        "Découvrez notre sélection de packs pour débutants en élevage de fourmis, incluant des fondations de différentes espèces et nids adaptés. Profitez d'un support professionnel et lancez-vous facilement dans la Myrmécologie avec nos packs complets !")

    bread = [pageAccueil, pagePack]
    pack_product = Pack_m.objects.filter(size__stock__gt=0, size__supplier__currently_available = True).distinct()
    country = []
    for pack in pack_product:
        if pack.sh_localisation() not in country:
            country.append(pack.sh_localisation())
    return render(request, 'sale/pack_product.html', context={"pack_product": pack_product, "country": country, 'meta':metat, "bread":bread})







def product_pack_detail_vi(request, id):
    """
    Render the pack product detail view.

    Args:
        request: The user's request object.
        id: The ID of the pack product.

    Returns:
        The rendered pack product detail view with context data.
    """
    # description_pack = "Le pack contient le nid, la fondation, une pince à épiler, une seringue, un morceau de 10 cm de tuyau pour les liaisons et une pipette"
    user = request.user
    pack_product = get_object_or_404(Pack_m, id=id)
    nest = pack_product.nest
    ant_product = pack_product.get_ant()
    price = pack_product.sh_price()

    comment = Feedback_m.objects.filter(
        Q(product_pack=pack_product) |
        Q(supplier=ant_product.supplier)  # Assurez-vous que votre modèle Product a un champ 'supplier'
    )

    metat = MetaTemplate(
        f"Pack Fourmis {pack_product.complete_spece()} de {pack_product.sh_localisation()} - Achat et Vente de Packs pour Élevage de Fourmis Débutants | Boutique en Ligne",
        f"Découvrez nos packs pour débutants incluant une fondation de fourmis {pack_product.complete_spece()} de {pack_product.sh_localisation()} et un nid adapté. Lancez-vous facilement dans l'élevage de fourmis avec notre pack complet et bénéficiez d'un support professionnel. Commandez dès maintenant !")

    pagePackDetails = Page("Pack détailles", '/produit/packs', 3, id)
    bread = [pageAccueil, pagePack, pagePackDetails]

    if ant_product.sh_problem() or pack_product.sh_problem():
        # Check problems
        messages.error(request, "désolée, nous avons un problème avec ce produit, nous travaillons dessus")
        return redirect("homepage_n")
    # List for offer ant, bottom
    offer_ant = offer_ant_func(pack_product, list(Ant_m.objects.filter(sizes__stock__gt=0).distinct()),
                               list(Pack_m.objects.filter(size__stock__gt=0).distinct()), list(Other_m.objects.filter(stock__gt=0).distinct()) )

    context = {"pack": pack_product, "price": price, "ant": ant_product, "offer_ant": offer_ant, 'meta': metat,
               "nest": nest, "bread": bread, "comment":comment}
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        # Check if the size is available
        res = pack_product.check_stock(quantity)
        if res:
            if user.is_authenticated:
                # Retrieve the ContentType for the product
                content_type = ContentType.objects.get_for_model(Pack_m)
                cart_item = OrderItem_m.objects.filter(
                    owner=user,
                    content_type=content_type,
                    object_id=pack_product.id,
                    is_ordered=False).first()
                match cart_item:
                    case None:
                        st = pack_product.check_stock(int(quantity))
                        if type(st) == bool:
                            cart_item = OrderItem_m.objects.create(owner=user, content_type=content_type,
                                                                   object_id=pack_product.id, quantity=quantity,
                                                                   price=price)
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {res}")
                            return render(request, 'sale/pack_detail.html', context)
                    case _:
                        res = pack_product.check_stock(int(quantity)+cart_item.quantity)
                        if res:
                            cart_item.quantity += int(quantity)
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {res}")
                            return render(request, 'sale/pack_detail.html', context)

                user_order, status = Order_m.objects.get_or_create(owner=user, is_ordered=False)
                user_order.items.add(cart_item)
                if status:
                    user_order.ref_code = generate_order_id()
                    user_order.save()
                messages.info(request, "article ajouté au panier")
                return redirect("homepage_n")
            else:
                return redirect("login_n")
        else:
            messages.error(request,
                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {res}")
    return render(request, 'sale/pack_detail.html',context)


def product_ant_detail_vi(request, id):
    """
    Render the ant product detail view.

    Args:
        request: The user's request object.
        id: The ID of the ant product.

    Returns:
        The rendered ant product detail view with context data.
    """
    user = request.user
    ant_product = get_object_or_404(Ant_m, id=id)
    comment = Feedback_m.objects.filter(
        Q(product_ant=ant_product) |
        Q(supplier=ant_product.supplier)  # Assurez-vous que votre modèle Product a un champ 'supplier'
    )
    metat = MetaTemplate(
        f"Achat Fourmis {ant_product.sh_spece()} {ant_product.under_spece} de {ant_product.sh_localisation()} - Vente Fondations et Colonies pour Débutants | Boutique en Ligne",
        f"Achetez des fondations de fourmis {ant_product.sh_spece()} {ant_product.under_spece} originaires de {ant_product.sh_localisation()} pour débutants. Parfait pour démarrer un élevage de fourmis. Livraison rapide et support professionnel. Rejoignez l'aventure de la Myrmécologie dès maintenant !")

    pageFourmisDetails = Page("Fourmis détailles", '/produit/fourmis', 3, id)
    bread = [pageAccueil, pageFourmis, pageFourmisDetails]
    if ant_product.sh_problem():
        # Check problems
        messages.error(request,
                       f"désolée, nous avons un problème avec ce produit, nous travaillons dessus")
        return redirect("homepage_n")
    # List for offer ant, bottom
    offer_ant = offer_ant_func(ant_product, list(Ant_m.objects.filter(sizes__stock__gt=0).distinct()),
                               list(Pack_m.objects.filter(size__stock__gt=0).distinct()), list(Other_m.objects.filter(stock__gt=0).distinct()) )

    context = {"ant": ant_product, "offer_ant": offer_ant, 'meta': metat, "bread": bread, "comment": comment}

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        size_id = request.POST.get('size_id')
        size = Size_m.objects.get(id=size_id)
        # Check if the size is available
        st = ant_product.check_stock(quantity, size)
        if st:
            if user.is_authenticated:
                # Check if the product with the same size is already in the user's cart
                content_type = ContentType.objects.get_for_model(Ant_m)
                cart_item = OrderItem_m.objects.filter(
                    owner=user,
                    content_type=content_type,
                    object_id=ant_product.id,
                    is_ordered=False).first()
                match cart_item:
                    case None:
                        st = ant_product.check_stock(int(quantity), size)
                        if type(st) == bool:
                            cart_item = OrderItem_m.objects.create(owner=user, content_type=content_type,
                                                                   object_id=ant_product.id, quantity=quantity,
                                                                   price=size.price)
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {st}")
                            return render(request, 'sale/ant_detail.html',context)

                    case _:
                        st = ant_product.check_stock(int(quantity) + cart_item.quantity, size)
                        if st:
                            cart_item.quantity += int(quantity)
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {st}")
                            return render(request, 'sale/ant_detail.html', context)

                user_order, status = Order_m.objects.get_or_create(owner=user, is_ordered=False)
                user_order.items.add(cart_item)
                if status:
                    user_order.ref_code = generate_order_id()
                    user_order.save()
                messages.info(request, "article ajouté au panier")
                return redirect("homepage_n")
            else:
                return redirect("login_n")
        else:
            messages.error(request,
                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {st}")
    return render(request, 'sale/ant_detail.html', context)




def product_other_detail_vi(request, id):
    """
    Render the other product detail view.

    Args:
        request: The user's request object.
        id: The ID of the other product.

    Returns:
        The rendered other product detail view with context data.
    """
    user = request.user
    other_product = get_object_or_404(Other_m, id=id)
    comment = Feedback_m.objects.filter(
        Q(product_other=other_product) |
        Q(supplier=other_product.supplier)  # Assurez-vous que votre modèle Product a un champ 'supplier'
    )
    metat = MetaTemplate(
        f"{other_product.type.capitalize()} pour élevage de Fourmis - {other_product.sh_name()} | Boutique en Ligne",
        f"Découvrez {other_product.sh_name()}, un {other_product.type} essentiel pour votre élevage de fourmis. Idéal pour les débutants, ce produit assure les meilleures conditions pour votre colonie. Explorez ses caractéristiques et profitez de nos offres exceptionnelles dès maintenant !"
    )

    pageOtherDetails = Page("Accessoires détailles", '/produit/accessoire', 3, id)
    bread = [pageAccueil, pageOther, pageOtherDetails]

    if other_product.sh_problem():
        # Check problems
        messages.error(request,
                       f"désolée, nous avons un problème avec ce produit, nous travaillons dessus")
        return redirect("homepage_n")
    # List for offer ant, bottom
    offer_ant = offer_other_func(other_product, list(Ant_m.objects.filter(sizes__stock__gt=0).distinct()),
                               list(Pack_m.objects.filter(size__stock__gt=0).distinct()), list(Other_m.objects.filter(stock__gt=0).distinct()) )

    context = {"other": other_product, "offer_ant": offer_ant, 'meta': metat, "bread": bread, "comment": comment}
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        # Check if the size is available
        st = other_product.check_stock(quantity)
        if st:
            if user.is_authenticated:
                # Check if the product with the same size is already in the user's cart
                content_type = ContentType.objects.get_for_model(Other_m)
                cart_item = OrderItem_m.objects.filter(
                    owner=user,
                    content_type=content_type,
                    object_id=other_product.id,
                    is_ordered=False).first()
                match cart_item:
                    case None :
                        st = other_product.check_stock(int(quantity))
                        if type(st) == bool:
                            cart_item = OrderItem_m.objects.create(owner=user, content_type=content_type,
                                                                   object_id=other_product.id, quantity=quantity,
                                                                   price=other_product.sh_price())
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {st}")
                            return render(request, 'sale/other_detail.html',
                                          context={"other": other_product, "offer_ant": offer_ant, 'meta': metat, "bread":bread, "comment": comment})
                    case _:
                        st = other_product.check_stock(int(quantity) + cart_item.quantity)
                        if st:
                            cart_item.quantity += int(quantity)
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {st}")
                            return render(request, 'sale/other_detail.html', context)

                user_order, status = Order_m.objects.get_or_create(owner=user, is_ordered=False)
                user_order.items.add(cart_item)
                if status:
                    user_order.ref_code = generate_order_id()
                    user_order.save()
                messages.info(request, "article ajouté au panier")
                return redirect("homepage_n")
            else:
                return redirect("login_n")
        else:
            messages.error(request,
                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {st}")
    return render(request, 'sale/other_detail.html', context)



@login_required
def cart_vi(request):
    """
    Render the cart view.

    Args:
        request: The user's request object.

    Returns:
        The rendered cart view with context data.
    """
    bread = [pageAccueil, pagePanier]
    existing_order = get_user_pending_order(request)
    match existing_order:
        case 0:
            return render(request, "sale/vacuum_cart.html")
        case _:
            match existing_order.is_ordered:
                case True:
                    return render(request, "sale/vacuum_cart.html")
                case False:
                    if existing_order.items.exists():
                        updated_items = existing_order.check_stock()
                        return render(request, "sale/cart.html", context={'items': updated_items, "order": existing_order, "bread":bread})
                    else:
                        return render(request, "sale/vacuum_cart.html")


@login_required()
def delete_cart_item_vi(request, item_id):
    """
    Delete an item from the cart.

    Args:
        request: The user's request object.
        item_id: The ID of the item to be deleted.

    Returns:
        A redirect to the cart view after deleting the item.
    """
    item_to_delete = OrderItem_m.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "L'article a été retiré du panier.")
    return redirect(reverse('cart_n'))
    

@login_required
def update_quantity(request):
    """
    Update the quantity of an item in the cart.

    Args:
        request: The user's request object.

    Returns:
        A redirect to the cart view after updating the quantity.
    """
    if request.method == "POST":
        form = UpdateQuantityForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            new_quantity = form.cleaned_data['new_quantity']
            item = get_object_or_404(OrderItem_m, id=item_id, owner=request.user)
            stock = item.get_stock()

            y = stock - new_quantity
            if y >= 0 :
                item.quantity = new_quantity
                messages.success(request, "La quantité a été mise à jour avec succès.")
                item.save()
            else :
                item.quantity = stock
                messages.warning(request,
                                 f"Il n'y a pas assez d'unités disponibles en stock, il ne nous en reste plus que {stock}.")
            return redirect('cart_n')
    else:
        return redirect('cart_n')


@login_required()
def checkout_vi(request):
    """
    Render the checkout view and handle address form submission.

    Args:
        request: The user's request object.

    Returns:
        The rendered checkout view with context data or a JSON response with new address data.
    """
    bread = [pageAccueil, pagePanier, pageCheckout]
    host = request.get_host()

    existing_order = get_user_pending_order(request)
    existing_order.shipping_type = "C"

    form = Address_fo()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': existing_order.get_cart_total(),
        'item_name': request.user,
        'invoice': uuid.uuid4(),
        'currency_code': 'EUR',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{'/produit/commande/success/'}{existing_order.id}",
        'cancel_url': f"http://{host}{'/produit/commande/checkout/'}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    if request.method == "POST":
        form = Address_fo(request.POST)
        if form.is_valid():

            new_address = form.save(commit=False)
            new_address.save()

            existing_order.address = new_address
            existing_order.save()
            existing_order.set_delivery_methode()
            shipping_costs = existing_order.shipping_costs()
            total = existing_order.get_cart_total()
            ze = "colis" 
            address_json = {
                "html": "\nPays : {}<br>\nNom complet : {}<br>\nNuméro de télephone : {}<br>\nAdresse : {}<br>\nDetails : {}<br>\nCode postal : {}<br>\nVille : {}<br>\n<hr>\n  Méthode de livraison : {}".format(
                    new_address.country, new_address.complete_name, new_address.phone_number, new_address.adress, new_address.postal_code, new_address.detail ,new_address.city, ze),
                "address_id": new_address.id,
                "total": total,
                "shipping_costs" : shipping_costs,
            }
            return JsonResponse(address_json)
        else:
            messages.error(request, "Le formulaire d'adresse est invalide.")
            
    if settings.WINTER :
        messages.success(request, "Attention, nous sommes en hiver : les décès dus au froid pendant la livraison ne sont plus remboursés. La livraison est effectuée avec une chaufferette.")

    context = {
        'order': existing_order,
        "form": form,
        "STRIPE_PUBLIC_KEY": os.environ.get('STRIPE_PUBLISHABLE_KEY'),
        "user": request.user,
        "bread":bread,
        'paypal': paypal_payment
    }

    return render(request, "sale/checkout.html", context)




@login_required
def success_vi(request, id):
    """
    Render the success view after a successful order and send an order email.

    Args:
        request: The user's request object.

    Returns:
        The rendered success view with context data.
    """

    order_ordered_vi(request, id)
    order = Order_m.objects.get(id=id)

    context = {
        'order': order,
        'user': request.user
    }

    return render(request, 'sale/success.html', context)


def orderEmail(request, user, to_email, order):
    """
    Send an email to the customer with the order details.

    Args:
        request: The user's request object.
        user: The user object.
        to_email: The recipient's email address.
        order: The order object.

    Returns:
        None
    """
    mail_subject = "Votre commande - Antly"

    order_items = order.get_cart_items()
    items_list = ""
    for item in order_items:
        items_list += f"{item.sh_name()} x {item.quantity} ({item.price}€)\n"

    address = order.address
    address_info = f"{address.complete_name}\n{address.adress}\n{address.detail}\n{address.postal_code} {address.city}\n{address.country}"

    context = {
        'user': user,
        'order': order,
        'items_list': items_list,
        'address_info': address_info
    }

    message = render_to_string('sale/email_template.txt', context)

    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(request,
                         f"Votre commande a été prise en compte, l'envoi de l'email à {to_email} est un succès.")
    else:
        messages.error(request, f"Erreur pour l'envoie de l'email à {to_email}")



@login_required
def createpayment(request):
    """
    Create a Stripe payment intent for the user's pending order.
    Args:
    request (HttpRequest): The request object containing user and session information.

    Returns:
        JsonResponse: A JSON response containing the client secret or an error message.
    """
    # Get the user's pending order
    order = get_user_pending_order(request)

    # Calculate the total order amount in cents
    amount = int(order.get_cart_total()) * 100

    # Ensure the total order amount is greater than zero
    if amount <= 0:
        return HttpResponse("Le montant total de la commande doit être supérieur à zéro.", status=400)

    # Set the Stripe API key
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    # Process the POST request
    if request.method == "POST":
        try:
            # Create the payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="eur",
                metadata={
                    "integration_check": "accept_a_payment",
                    "order_id": order.id,
                    'profile_id': request.user.id
                },
            )

            # Return the client secret for the payment intent
            return JsonResponse({"clientSecret": payment_intent["client_secret"]})
        except Exception as e:
            # Return an error message in case of an exception
            return JsonResponse({"error": str(e)})


@csrf_exempt
def webhook_vi(request):
    """
    Handle Stripe webhook events for successful payment intents.
    Args:
    request (HttpRequest): The request object containing webhook data.

    Returns:
        HttpResponse: An HTTP response with a status code indicating success or failure.
    """
    # Get the webhook payload and signature header
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        # Construct the webhook event
        event = stripe.Webhook.construct_event(payload, sig_header,'whsec_iG1a7cIlmL5RcFYB1Wn03QiX4FIdmXHn')
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    return HttpResponse(status=200)




def order_ordered_vi(request, id):

    """all operation to do after after sucess"""

    order = Order_m.objects.get(id=id)
    if not order.is_ordered :

        # Get the user's last order
        address = order.address
        orderEmail(request, request.user, request.user.email, order)

        # Check if the order exists
        if not order:
            messages.error(request, "No order found.")
            return redirect('checkout_n')

        # Set up the credentials
        credentials = service_account.Credentials.from_service_account_file(
            settings.BASE_DIR / "google_json/credentials.json",
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )

        # Create a client object to interact with the API
        sheets = build('sheets', 'v4', credentials=credentials)

        # Your Google Sheets spreadsheet ID
        spreadsheet_id = '19amsgc6XnQI-zJ1tZU_ZyIilywxTi6xwupygYH2SZGU'

        # The tab name where you want to add the order information
        sheet_name = 'order'

        # The order information you want to add
        date_ordered = order.date_ordered.strftime('%Y-%m-%d %H:%M:%S')
        customer_name = f"{address.complete_name}"
        items = order.get_cart_items()
        order_contents = ", ".join([f"{item.sh_name()} de {item.sh_supplier()} x {item.quantity} ({item.price}€)" for item in items])
        address = order.address
        address_info = f"{address.complete_name}, {address.adress}, {address.detail}, {address.postal_code} {address.city}, {address.country}"
        contact = f"{address.phone_number} | {request.user.email}"
        to = sum(i.price for i in order.get_cart_items())
        total = f"{to}"
        total_ship = f"{to + order.shipping_costs()}"
        order_data = [date_ordered, customer_name, order_contents, address_info, contact, total, total_ship]

        # Add the order information to the spreadsheet
        requeste = sheets.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [order_data]}
        )

        response = requeste.execute()

        # send mail to supplier
        def percentage(value):
            percentage_value = Decimal(100 - settings.PERCENT_ANTLY) / 100
            return value * percentage_value

        supplierl = []
        for y in order.get_cart_items() :
            id = y.show_supplier_id()
            supplier = Supplier_m.objects.get(pk=id)
            supplierl.append(supplier)


        for i in supplierl :
            id = i.id
            iteml= []
            for e in items :
                if e.show_supplier_id() == id:
                    iteml.append(e)

            px = 0
            for u in iteml :
                px += u.price
            supplier = Supplier_m.objects.get(pk=id)
            user = supplier.user
            orderr = ", ".join([f"{item.sh_name()} x {item.quantity} ({item.price}€)" for item in iteml])
            message = f"""
            passé le {date_ordered} 
                    
            Adresse du client {address_info} 
            
            prix facturé au client : {px}
            Pourcentage pris par Antly : {settings.PERCENT_ANTLY} %
            Votre gain (les frais de port restent à votre charge) : {percentage(px)}
            
            Contenu de la commande :
            {orderr}

            contact : 
            {contact}
            
            
            Rappel :
            
            Vous devez envoyer le colis via La Poste. Ensuite, rendez-vous sur votre interface fournisseur à l'adresse "https://www.antly.fr/admin/" pour créer un "OrderTrack_m" et y renseigner votre numéro de suivi.
            
            Pour me contacter :
            06 51 33 61 58
            """
            user.email_user(f"Antly - Nouvelle commande passée le {order.date_ordered}", message)



                # Update the placed order
            order.is_ordered = True
            order.date_ordered = timezone.now().date()
            order.save()

            # Get all items in the order (generates a queryset)
            order_items = order.items.all()

            # Update order items
            order_items.update(is_ordered=True)

            # Reduce stock for each item in the order
            for item in order_items:
                item.reduce_stock()

            # Create a transaction
            transaction = Transaction(shopper=request.user,
                                    order=order,
                                    success=True)

            # Save the transaction
            transaction.save()



def seller_vi(request, id):

    
    pageSellerDetails = Page("Vendeur détaille", '/seller/', 2, id)
    bread = [pageVendeur, pageSellerDetails]
    products = get_products_for_supplier(id)
    supplier = Supplier_m.objects.get(id=id)
    
    context = {
        'product': products,
        'seller': supplier,
        'bread': bread
    }
    return render(request, 'sale/seller.html', context)


def seller_all_vi(request):

    metat = MetaTemplate(
        "Fondations de Fourmis pour Débutants - Achat et Vente de Colonies de Fourmis | Boutique en Ligne",
        "Explorez notre collection de fondations de fourmis pour débutants, avec une variété d'espèces et d'origines. Démarrez votre élevage de fourmis en toute simplicité et bénéficiez d'un support professionnel. Découvrez nos offres dès maintenant !")

    bread = [pageVendeur]
    available_suppliers = Supplier_m.objects.filter(currently_available=True)


    context = {
        'suppliers': available_suppliers,
        'bread': bread
    }
    return render(request, 'sale/seller_all.html', context)



@login_required
def generate_invoice_pdf(request, order_id):
    # Récupérez la commande en fonction de l'order_id
    order = Order_m.objects.get(id=order_id)
    address = order.address

    # Créez un fichier PDF en mémoire
    buffer = io.BytesIO()

    # Créez le fichier PDF en utilisant la bibliothèque ReportLab
    p = canvas.Canvas(buffer)


    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, "Facture")

    # 2. Informations sur le vendeur
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 750, "Informations du vendeur")
    p.setFont("Helvetica", 12)
    p.drawString(50, 730, f"Vendeur: {settings.COMPANY_NAME}")
    p.drawString(50, 715, f"Adresse: {settings.COMPANY_ADDRESS}")
    p.drawString(50, 700, f"Téléphone: {settings.COMPANY_PHONE}")
    p.drawString(50, 685, f"Email: {settings.COMPANY_EMAIL}")
    p.drawString(50, 670, f"SIRET/SIREN: {settings.COMPANY_SIRET}")
    p.drawString(50, 655, f"Numéro de TVA: {settings.COMPANY_VAT_NUMBER}")

    # 3. Informations sur le client
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 615, "Informations du client")
    p.setFont("Helvetica", 12)
    p.drawString(50, 595, f"Client : {address.complete_name}")
    if not address.detail:
        p.drawString(50, 580, f"Adresse: {address.complete_name} {address.adress} {address.postal_code} {address.city} {address.country}")
    else:
        p.drawString(50, 580, f"Adresse: {address.complete_name} {address.adress} ({address.detail}) {address.postal_code} {address.city} {address.country}")
    p.drawString(50, 565, f"Téléphone: {address.phone_number}")
    p.drawString(50, 550, f"Email: {order.owner.email}")
    # Ajoutez ici le numéro de TVA du client si applicable

    # 4. Barre de séparation
    p.setLineWidth(2)
    p.line(50, 535, 550, 535)

    # 5. Dates et numéro de facture
    p.setFont("Helvetica", 12)
    p.drawString(50, 515, f"Date de facturation : {order.date_ordered.strftime('%d/%m/%Y')}")
    p.drawString(50, 500, f"Numéro de facture : {order.ref_code}")

    # 6. Tableau des produits ou services
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 475, "Description des produits ou services:")
    p.setFont("Helvetica", 12)

    # Coordonnées de départ pour les produits ou services
    x = 50
    y = 455

    # Ajoutez ici les produits ou services, avec la quantité, le prix unitaire et le prix total
    for item in order.get_cart_items():
        p.drawString(x, y, f"{item.sh_name()}")
        p.drawString(x + 200, y, f"{item.quantity}")
        p.drawString(x + 300, y, f"{item.price} €")
    y -= 20
    # Ajoutez les frais de transport
    p.drawString(x, y, "Transport")
    p.drawString(x + 200, y, "")
    p.drawString(x + 300, y, f"{order.shipping_costs()} €")
    y -= 20

    if settings.FREE_COLONIE and order.gift:
        p.drawString(x, y, "Colonie offerte")
        p.drawString(x + 200, y, "1")
        p.drawString(x + 300, y, "0 €")
        y -= 20

    # Affichez le total de la commande
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "Total de la commande")
    p.drawString(x + 300, y, f"{order.get_order_total()} €")

    # 7. Conditions générales et politique de retour
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 360, "Conditions générales et politique de retour")
    p.setFont("Helvetica", 12)
    p.drawString(50, 345, "Veuillez consulter notre site web pour plus d'informations :")
    p.setFont("Helvetica-Oblique", 12)
    p.drawString(50, 330, "https://www.antly.fr")

    # Terminez le fichier PDF
    p.showPage()
    p.save()

    # Créez la réponse avec le fichier PDF en mémoire
    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=facture_{order.ref_code}.pdf'

    return response

