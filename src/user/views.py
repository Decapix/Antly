from allauth.account.forms import default_token_generator
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse
from .decorators import user_not_authenticated
from .forms import *
from .models import *
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from super.models import MetaTemplate
from sale.modelcart import Order_m


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Merci pour votre confirmation par e-mail. Votre compte à été crée")
        login(request, user)
        return redirect('homepage_n')
    else:
        messages.error(request, "Lien d'activation invalide")

    return redirect('homepage_n')


def activateEmail(request, user, to_email):
    mail_subject = "Activez votre compte utilisateur."
    message = render_to_string("user/template_activate_account.html", {
        'user': user.username(),
        # 'domain': get_current_site(request).domain,
        'domain': "antly.fr",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"L'envoi de l'email à {to_email} est un succès, veuillez regarder dans votre boite "
                                  f"mail ")
    else:
        messages.error(request,
                       f"Problème d'envoi de l'email à {to_email}, vérifiez si vous l'avez entré correctement.")


def changepasswordEmail(request, user, to_email):
    mail_subject = "Confirmer votre identitée"
    message = render_to_string("user/template_change_password.html", {
        'user': user.username,
        # 'domain': get_current_site(request).domain,
        'domain': "antly.fr",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"L'envoi de l'email à {to_email} est un succès, veuillez regarder dans votre boite "
                                  f"mail ")
    else:
        messages.error(request,
                       f"Problème d'envoi de l'email à {to_email}, vérifiez si vous l'avez entré correctement.")



@user_not_authenticated
def signup_vi(request):
    """view for signup"""
    metat = MetaTemplate(
        f"Inscription - Créez votre compte | Boutique en Ligne de Fourmis pour Débutant",
        f"Inscrivez-vous sur notre boutique en ligne de fourmis pour débutants et profitez d'offres exclusives, suivez vos commandes et gérez votre compte. Rejoignez la communauté des passionnés de Myrmécologie et démarrez votre élevage de fourmis dès aujourd'hui !")

    if request.method == "POST":
        form = Signup_fo(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("homepage_n")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = Signup_fo()
    return render(request, 'user/signup.html', context={'form': form, "meta": metat})



@login_required
def logout_vi(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès")
    return redirect("homepage_n")

@login_required
def delete_user_vi(request, pk):
    user = Shopper_m.objects.get(id=pk)
    user.delete()
    messages.info(request, "Vous avez supprimé votre compte avec succès, hâte de vous revoir sous une nouvelle "
                           "identitée")
    return redirect('homepage_n')


@user_not_authenticated
def login_vi(request):
    """login"""
    metat = MetaTemplate(
        f"Connexion - Boutique en Ligne de Fourmis pour Débutants | Élevage de Fourmis et Accessoires",
        f"Connectez-vous à votre compte sur notre boutique en ligne de fourmis pour gérer vos commandes, suivre vos expéditions et accéder à des offres exclusives. Inscrivez-vous dès maintenant pour commencer votre aventure en Myrmécologie !")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Bonjour {user.username}! Vous avez bien été connecté")

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("homepage_n")
        else:
            messages.success(request, "votre email ou votre mot de passe est erronée")
    return render(request, 'user/login.html', context={"meta": metat})


@user_not_authenticated
def password_reset_request_vi(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = Shopper_m.objects.filter(email=email).first()
        if user:
            changepasswordEmail(request, user, email)
            return redirect("homepage_n")
        else:
            messages.error(request, "Aucun utilisateur trouvé avec cet email.")
    return render(request, "user/password_reset_request.html")



def change_password_vi(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    password_form = NewPassword_fo(user=user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        if request.method == "POST":
            password_form = NewPassword_fo(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                login(request, user)
                messages.success(request, "Vous avez modifiez votre mot de passe avec succès")
                return redirect('homepage_n')
    else:
        messages.error(request, "Lien d'activation invalide")

    return render(request, 'user/change_password.html', context={"form": password_form, "user": user, "password_form": password_form})


@login_required
def dashboard_vi(request, pk):
    """view for account dashboard"""
    user = Shopper_m.objects.get(id=pk)
    form = WhyAnt_fo(instance=user)
    if request.method == "POST":
        form = WhyAnt_fo(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard_n', kwargs={"pk": user.id}))
    return render(request, 'user/dashboard.html', context={"form": form})


@login_required
def detail_vi(request, pk):
    """detail"""
    user = Shopper_m.objects.get(id=pk)
    form = Detail_fo(instance=user)
    password_form = UpdatePassword_fo(user=user)
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'detail':
            form = Detail_fo(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Vous avez modifiez votre profile avec succès")
                return redirect(reverse('detail_n', kwargs={"pk": user.id}))
            else:
                messages.error(request, "Erreur lors de la validation du formulaire :")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        if form_type == 'password':
            password_form = UpdatePassword_fo(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                login(request, user)
                messages.success(request, "Vous avez modifiez votre mot de passe avec succès")
                return redirect(reverse('detail_n', kwargs={"pk": user.id}))
            else:
                messages.error(request, "Erreur lors de la validation du formulaire :")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        else:
            password_form = UpdatePassword_fo(user=user)

    return render(request, 'user/detail.html', context={"form": form, "user": user, "password_form": password_form})


@login_required
def orders_vi(request, pk):
    """orders placed"""
    user = Shopper_m.objects.get(id=pk)
    orders = Order_m.objects.filter(owner=request.user, is_ordered=True)
    return render(request, 'user/orders.html', context={"user": user, "orders":orders})

"""
@login_required
def address_vi(request, pk):
    user = Shopper_m.objects.get(id=pk)
    if user.address_m_set.exists():
        if request.method == "POST":
            form = Address_fo(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.shopper = request.user
                address.save()
                return redirect(reverse('address_n', kwargs={"pk": user.id}))
        else:
            form = Address_fo()
        return render(request, 'user/address.html', context={"form": form, "user": user})

    else:
        if request.method == "POST":
            form = Address_fo(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.shopper = request.user
                address.save()
                return redirect(reverse('address_n', kwargs={"pk": user.id}))
        else:
            form = Address_fo()

        return render(request, 'user/address.html', context={"form": form})
"""

@login_required
def delete_account_vi(request, pk):
    user = Shopper_m.objects.get(id=pk)
    return render(request, 'user/delete_account.html', context={"user": user})


def comment_vi(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = Feedback_fo(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.shopper = user
                feedback.save()
                messages.success(request, "Votre retour est envoyé, merci !")
                return redirect('homepage_n')
        else:
            form = Feedback_fo()

        context = {'form': form}
        return render(request, 'user/comment.html', context)
    else:
        return redirect("login_n")





