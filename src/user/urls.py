from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('connexion/', login_vi, name="login_n"),
    path('déconnexion/', logout_vi, name="logout_n"),
    path('<str:pk>/suppression/', delete_user_vi, name='delete_user_n'),
    path('inscription/', signup_vi, name="signup_n"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('compte/<str:pk>', dashboard_vi, name="dashboard_n"),
    path('compte/<str:pk>/commandes/', orders_vi, name="orders_n"),
    path('compte/<str:pk>/detailes/', detail_vi, name="detail_n"),
    # path('compte/<str:pk>/adresse/', address_vi, name="address_n"),
    path('compte/commentaire/', comment_vi, name="comment_n"),
    path('compte/<str:pk>/supprimer_mon_compt/', delete_account_vi, name="delete_account_n"),
    path('password-reset/', password_reset_request_vi, name='password_reset_request_n'),
    path('password-change/<uidb64>/<token>', change_password_vi, name='change_password_n'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)