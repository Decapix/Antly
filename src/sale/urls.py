from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('panier/', cart_vi, name="cart_n"),
    path('panier/supprimer/<str:item_id>/produit/', delete_cart_item_vi, name="delete_cart_item_n"),
    path('fourmis/', ant_product_vi, name="ant_product_n"),
    path('packs/', pack_product_vi, name="pack_product_n"),
    path('accessoire/', other_product_vi, name="other_product_n"),
    path('fourmis/<str:id>/', product_ant_detail_vi, name="ant_detail_n"),
    path('packs/<str:id>/', product_pack_detail_vi, name="pack_detail_n"),
    path('accessoire/<str:id>/', product_other_detail_vi, name="other_detail_n"),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('commande/checkout/', checkout_vi, name="checkout_n"),
    path('commande/success/<str:id>/', success_vi, name="success_n"),
    path("commande/create-payment-intent/", createpayment, name="create-payment-intent"),
    path("commande/webhook/", webhook_vi, name="webhook"),
    path('facture/<str:order_id>/', generate_invoice_pdf, name='facture_pdf'),
    # path('commande/create-paypal-payment/', create_paypal_payment, name="create-paypal-payment"),
    # path('commande/process-paypal-payment/',process_paypal_payment, name="process-paypal-payment"),
    path("seller/<str:id>", seller_vi, name="seller_n"),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

