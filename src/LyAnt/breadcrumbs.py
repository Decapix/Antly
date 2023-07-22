from django.urls import reverse


class Page :
    def __init__(self, name, link, position, id=None):
        self.name = name
        self.link = reverse(link, kwargs={'id': id}) if id else reverse(link)
        self.position = position

page = Page("", reverse('_n'), 1)

pageAccueil = Page("Accueil", 'homepage_n', 1)
pageInformation = Page("Informations", 'information_n', 2)
pageCvg = Page("Conditions générale de ventes", 'cgv_n', 3)
pageChoisir = Page("Choisir son espèce", 'specie_form_n', 2)

pageAvis = Page("Avis", 'comment_n', 3)

pagePanier = Page("Panier", 'cart_n', 2)
pageFourmis = Page("Fourmis", 'ant_product_n', 2)
pagePack = Page("Pack", 'pack_product_n', 2)
pageOther = Page("Accessoires", 'other_product_n', 2)
pagePackDetails = Page("Pack détailles", 'product_pack_detail_n', 3)
pageOtherDetails = Page("Accessoires détailles", 'product_other_detail_n', 3)
pageCheckout = Page("Résumé de la commande", 'checkout_n', 3)



