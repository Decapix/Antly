from django.urls import reverse


class Page :
    def __init__(self, name, link, position, id=None):
        self.name = name
        self.link = f'{link}/{id}' if id else f'{link}'
        self.position = position


pageAccueil = Page("Accueil", '/', 1)
pageInformation = Page("Informations", '/information/', 2)
pageCvg = Page("Conditions générale de ventes", '/information/cgv/', 3)
pageChoisir = Page("Choisir son espèce", '/information/choisir', 2)

pageAvis = Page("Avis", '/utilisateur/compte/commentaire/', 3)

pageFourmis = Page("Fourmis", '/produit/fourmis/', 2)
pagePack = Page("Pack", '/produit/packs/', 2)
pageOther = Page("Accessoires", '/produit/accessoire/', 2)
pagePanier = Page("Panier", '/produit/panier/', 2)
pageCheckout = Page("Résumé de la commande", '/produit/commande/checkout/', 3)
