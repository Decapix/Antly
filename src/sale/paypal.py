# paypal.py
import paypalrestsdk
from django.conf import settings


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})


def create_paypal_transaction(order):
    # Configurez le SDK de PayPal
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    items = [
        {'name': item.name(), 'sku': str(item.id), 'price': str(item.price), 'currency': "EUR", 'quantity': item.quantity}
        for item in order.get_cart_items()]

    # Créez la transaction PayPal

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "https://www.antly.fr/produit/commande/success/",
            "cancel_url": "https://www.antly.fr/produit/commande/checkout/"},
        "transactions": [{
            "item_list": {
                "items": items},
            "amount": {
                "total": "10",
                "details": {
                    "subtotal": "7",
                    "shipping": "3",
                },
                "currency": "EUR"},
            "description": "commande fourmis antly"}]})


    if not payment.create():
        print(payment.error)  # Imprime l'erreur de PayPal
        return None
    return payment



def execute_paypal_transaction(payment_id, payer_id):
    # Configurez le SDK de PayPal
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    # Récupérez la transaction PayPal
    payment = paypalrestsdk.Payment.find(payment_id)

    # Exécutez la transaction PayPal
    return payment if payment.execute({"payer_id": payer_id}) else None
