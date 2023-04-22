from django.contrib.auth.decorators import login_required
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

    ant_product = Ant_m.objects.filter(sizes__stock__gt=0).distinct()
    country = []
    for ant in ant_product:
        if ant.localisation not in country:
            country.append(ant.localisation)
    return render(request, 'sale/ant_product.html', context={"ant_product": ant_product, "country": country, 'meta':metat})


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

    pack_product = Pack_m.objects.filter(size__stock__gt=0).distinct()
    country = []
    for ant in pack_product:
        if ant.localisation not in country:
            country.append(ant.localisation())
    return render(request, 'sale/pack_product.html', context={"pack_product": pack_product, "country": country, 'meta':metat})



def product_pack_detail_vi(request, id):
    """
    Render the pack product detail view.

    Args:
        request: The user's request object.
        id: The ID of the pack product.

    Returns:
        The rendered pack product detail view with context data.
    """
    user = request.user
    pack_product = get_object_or_404(Pack_m, id=id)
    size = pack_product.size
    ant_product = pack_product.get_ant()
    price = pack_product.get_price()
   metat = MetaTemplate(
        f"Pack Fourmis {pack_product.complete_spece()} de {pack_product.localisation()} - Achat et Vente de Packs pour Élevage de Fourmis Débutants | Boutique en Ligne",
        f"Découvrez nos packs pour débutants incluant une fondation de fourmis {pack_product.complete_spece()} de {pack_product.localisation()} et un nid adapté. Lancez-vous facilement dans l'élevage de fourmis avec notre pack complet et bénéficiez d'un support professionnel. Commandez dès maintenant !")
 
    if ant_product.problem or pack_product.problem:
        # Check problems
        messages.error(request, "désolée, nous avons un problème avec ce produit, nous travaillons dessus")
        return redirect("homepage_n")
    # List for offer ant, bottom
    offer_ant = offer_ant_func(ant_product, list(Ant_m.objects.filter(sizes__stock__gt=0).distinct()), list(Pack_m.objects.filter(size__stock__gt=0).distinct()))
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        # Check if the size is available
        if int(size.stock) - int(quantity) >= 0:
            if user.is_authenticated:
                # Check if the product with the same size is already in the user's cart
                cart_item = OrderItem_m.objects.filter(owner=user, product=ant_product, size=size, pack=pack_product, is_ordered=False).first()
                match cart_item:
                    case None:
                        cart_item = OrderItem_m.objects.create(owner=user, product=ant_product, quantity=quantity, price=price)
                        cart_item.size.add(size)
                        cart_item.pack.add(pack_product)
                        cart_item.save()
                    case _:
                        if int(size.stock) - (int(quantity) + cart_item.quantity) >= 0:
                            cart_item.quantity += int(quantity)
                            cart_item.save()
                        else:
                             messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {size.stock}")
                            return render(request, 'sale/pack_detail.html', context={"pack": pack_product, 'meta':metat, "price": price, "ant": ant_product, "offer_ant": offer_ant})

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
                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {size.stock}")
    return render(request, 'sale/pack_detail.html', context={"pack": pack_product, "price": price, "ant": ant_product, "offer_ant": offer_ant, 'meta':metat})



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
    metat = MetaTemplate(
        f"Achat Fourmis {ant_product.spece} {ant_product.under_spece} de {ant_product.localisation} - Vente Fondations et Colonies pour Débutants | Boutique en Ligne",
        f"Achetez des fondations de fourmis {ant_product.spece} {ant_product.under_spece} originaires de {ant_product.localisation} pour débutants. Parfait pour démarrer un élevage de fourmis. Livraison rapide et support professionnel. Rejoignez l'aventure de la Myrmécologie dès maintenant !")

    if ant_product.problem:
        # Check problems
        messages.error(request,
                       f"désolée, nous avons un problème avec ce produit, nous travaillons dessus")
        return redirect("homepage_n")
    # List for offer ant, bottom
    offer_ant = offer_ant_func(ant_product, list(Ant_m.objects.filter(sizes__stock__gt=0).distinct()), list(Pack_m.objects.filter(size__stock__gt=0).distinct()))
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        size_id = request.POST.get('size_id')
        size = Size_m.objects.get(id=size_id)
        # Check if the size is available
        if int(size.stock) - int(quantity) >= 0:
            if user.is_authenticated:
                # Check if the product with the same size is already in the user's cart
                cart_item = OrderItem_m.objects.filter(owner=user, product=ant_product, size=size, pack__isnull=True, is_ordered=False).first()
                match cart_item:
                    case None:
                        cart_item = OrderItem_m.objects.create(owner=user, product=ant_product, quantity=quantity, price=size.price)
                        cart_item.size.add(size)
                        cart_item.save()
                    case _:
                        if int(size.stock) - (int(quantity) + cart_item.quantity) >= 0:
                            cart_item.quantity += int(quantity)
                            cart_item.save()
                        else:
                            messages.error(request,
                                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {size.stock}")
                            return render(request, 'sale/ant_detail.html',
                                          context={"ant": ant_product, "offer_ant": offer_ant, 'meta':metat})

                user_order, status = Order_m.objects.get_or_create(owner=user, is_ordered=False)
                user_order.items.add(cart_item)
                if status:
                    user_order.ref_code = generate_order_id()
                    user_order.save()
                messages.info(request, "item added to cart")
                return redirect("homepage_n")
            else:
                return redirect("login_n")
        else:
            messages.error(request,
                           f"désolée, nous n'avons plus assez d'unitées en stock, il nous en reste {size.stock}")
    return render(request, 'sale/ant_detail.html', context={"ant": ant_product, "offer_ant": offer_ant, 'meta':metat})


@login_required
def cart_vi(request):
    """
    Render the cart view.

    Args:
        request: The user's request object.

    Returns:
        The rendered cart view with context data.
    """
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
                        items = existing_order.items.all()

                        return render(request, "sale/cart.html", context={'items': items, "order": existing_order})
                    else:
                        return render(request, "sale/vacuum_cart.html")


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

            # Find the size associated with the item
            size = item.size.first()

            if size.stock is not None and new_quantity > size.stock:
                messages.error(request, "Il n'y a pas assez d'unités disponibles en stock pour cette taille.")
            else:
                item.quantity = new_quantity
                item.save()

            return redirect('cart_n')
    else:
        return redirect('cart_n')


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
    

@login_required()
def checkout_vi(request):
    """
    Render the checkout view and handle address form submission.

    Args:
        request: The user's request object.

    Returns:
        The rendered checkout view with context data or a JSON response with new address data.
    """
    existing_order = get_user_pending_order(request)
    form = Address_fo()

    if request.method == "POST":
        form = Address_fo(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.save()

            existing_order.address = new_address
            existing_order.save()

            address_json = {
                "html": "\nCountry/Region : {}<br>\nFull name : {}<br>\nPhone number : {}<br>\nAddress : {}<br>\nDetail : {}<br>\nPostal code : {}<br>\nCity : {}<br>\n".format(
                    new_address.country, new_address.complete_name, new_address.phone_number, new_address.adress, new_address.postal_code, new_address.detail ,new_address.city),
                "address_id": new_address.id
            }
            return JsonResponse(address_json)
        else:
            messages.error(request, "Le formulaire d'adresse est invalide.")

    context = {
        'order': existing_order,
        "form": form,
        "STRIPE_PUBLIC_KEY": os.environ.get('STRIPE_PUBLIC_KEY'),
        "user": request.user
    }

    return render(request, "sale/checkout.html", context)


@login_required
def success_vi(request):
    """
    Render the success view after a successful order and send an order email.

    Args:
        request: The user's request object.

    Returns:
        The rendered success view with context data.
    """
    # Get the user's last order
    order = Order_m.objects.filter(owner=request.user).order_by('-date_ordered').first()
    address = order.address
    orderEmail(request, request.user, request.user.email, order)

    # Check if the order exists
    if not order:
        messages.error(request, "No order found.")
        return redirect('checkout_n')

    # Set up the credentials
    credentials = service_account.Credentials.from_service_account_file(
        settings.BASE_DIR / "google_json/antly-address-c82b73d4440d.json",
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
    order_contents = ", ".join([f"{item.name()} x {item.quantity} ({item.price}€)" for item in order.get_cart_items()])
    address = order.address
    address_info = f"{address.complete_name}, {address.adress}, {address.detail}, {address.postal_code} {address.city}, {address.country}"
    contact = f"{address.phone_number} | {request.user.email}"

    order_data = [date_ordered, customer_name, order_contents, address_info, contact]

    # Add the order information to the spreadsheet
    requeste = sheets.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [order_data]}
    )

    response = requeste.execute()

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
        items_list += f"{item.name()} x {item.quantity} ({item.price}€)\n"

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
        event = stripe.Webhook.construct_event(payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET'))
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event if it's a successful payment intent
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        order_id = payment_intent.metadata["order_id"]

        # Get the order and user profile associated with the payment intent
        order_to_purchase = Order_m.objects.get(id=order_id)
        profile_id = payment_intent.metadata['profile_id']
        user_profile = Profile.objects.get(id=profile_id)

        # Update the placed order
        order_to_purchase.is_ordered = True
        order_to_purchase.date_ordered = timezone.now().date()
        order_to_purchase.save()

        # Get all items in the order (generates a queryset)
        order_items = order_to_purchase.items.all()

        # Update order items
        order_items.update(is_ordered=True)

        # Reduce stock for each item in the order
        for item in order_items:
            for size in item.size.all():
                size.stock -= item.quantity
                size.save()

        # Create a transaction
        transaction = Transaction(shopper=user_profile,
                                  order=order_to_purchase,
                                  success=True)

        # Save the transaction
        transaction.save()

    return HttpResponse(status=200)



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
        p.drawString(x, y, f"{item.name()}")
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

