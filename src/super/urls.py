from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.conf import settings


urlpatterns = [
    path('', homepage_vi, name="homepage_n"),
    path('information/', information_vi, name="information_n"),
    path('information/cgv/', cgv_vi, name="cgv_n"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)