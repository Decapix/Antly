from django.contrib.auth import authenticate, password_validation
from django.forms import TextInput, EmailInput, PasswordInput
from django.utils.translation import gettext_lazy as _
from .models import Address_m

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm

from .models import *
from django import forms


class Signup_fo(UserCreationForm):
    class Meta:
        model = Shopper_m
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'mot de passe',
            "onclick": "changer1()",
            "id": "password1",
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'mot de passe',
            "onclick": "changer2()",
            "id": "password2",
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
        })

    def save(self, commit=True):
        users = super(Signup_fo, self).save(commit=False)
        users.email = self.cleaned_data['email']

        if commit:
            users.save()
        return users


class Login_fo(forms.Form):
    """
    class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """

    email = forms.CharField(
        label="email",
        strip=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )

    password = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Password'}),
    )

    error_messages = {
        "invalid_login": _(
            "Veuillez saisir un %(email)s et un mot de passe corrects. Notez que les deux peuvent être sensibles à la casse."
        ),
        "inactive": _("Ce compte est inactif."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )


class WhyAnt_fo(forms.ModelForm):
    class Meta:
        model = Shopper_m
        fields = ['favorite_specie', 'why_ant']
        widgets = {
            'favorite_specie': TextInput(attrs={
                'class': "form-control mt-4 mb-4",
                'required': "False",
                'placeholder': "Espèce favorite",
            }),
            'why_ant': TextInput(attrs={
                'class': "form-control mt-4 mb-4",
                'rows': "3",
                'required': "False",
                'placeholder': "Pouquoi ?",
            }),
        }


class Detail_fo(forms.ModelForm):
    class Meta:
        model = Shopper_m
        fields = ['last_name', 'first_name', 'username']

        widgets = {
            'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Nom",
                'required': "False"
            }),
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Prénom",
                'required': "False"
            }),
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Nom d'utilisateur",
                'required': "False"
            }),
        }


class UpdatePassword_fo(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "id": "password2", "class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirmation Nouveau mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "id": "password3", "class": "form-control"}),
    )

    old_password = forms.CharField(
        label=_("Encien mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, "id": "password1", "class": "form-control"}
        ),
    )


class NewPassword_fo(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control", "id": "password1", }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirmation Nouveau mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control", "id": "password2", }),
    )


class Address_fo(forms.ModelForm):
    class Meta:
        model = Address_m
        fields = ['country', 'complete_name', 'phone_number', 'adress', 'detail', 'postal_code', 'city', ]

        widgets = {
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Pays/Région (ex : France)')
            }),
            'complete_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nom complet (ex : Bernard Weber)')
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Numéro de téléphone (ex : 0660066006)')
            }),
            'adress': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Adresse (ex : 6 sentier de la fourmis)')
            }),
            'detail': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Détail (ex : batiment 2) *facultatif*')
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Code postal (ex : 59610)')
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ville (ex : Fourmies)')
            }),
        }


class Feedback_fo(forms.ModelForm):
    class Meta:
        model = Feedback_m
        fields = ['text', 'star', 'shopper', 'supplier', 'antly', 'product_ant', 'product_other', 'product_pack']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre avis...', 'rows': 4}),
            'star': forms.HiddenInput(),
            'shopper': forms.HiddenInput(),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'antly': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'product_ant': forms.Select(attrs={'class': 'form-control'}),
            'product_other': forms.Select(attrs={'class': 'form-control'}),
            'product_pack': forms.Select(attrs={'class': 'form-control'}),
        }

