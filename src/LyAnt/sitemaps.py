from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from sale.models import Ant_m, Pack_m
from user.models import Shopper_m
from super.models import Offer_m


class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['homepage_n', 'information_n', 'cgv_n', 'login_n', 'signup_n']

    def location(self, item):
        return reverse(item)


class AntSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Ant_m.objects.all()

    def location(self, item):
        return reverse('ant_detail_n', args=[str(item.id)])


class PackSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Pack_m.objects.all()

    def location(self, item):
        return reverse('pack_detail_n', args=[str(item.id)])


class ShopperSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Shopper_m.objects.all()

    def location(self, item):
        return reverse('dashboard_n', args=[str(item.id)])


class OfferSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Offer_m.objects.all()

    def location(self, item):
        return reverse('information_n', args=[str(item.id)])


sitemaps = {
    'static': StaticSitemap,
    'ants': AntSitemap,
    'packs': PackSitemap,
    'shoppers': ShopperSitemap,
    'offers': OfferSitemap,
}
