"""
Django settings for LyAnt project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary_storage
# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4o949ijfccf)w8ll%(hgb#b%h29p#g69dljf*)af9pkd1f_iw5'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get('ENV') != 'PRODUCTION'
DEBUG = True
ALLOWED_HOSTS = ['antly.herokuapp.com', 'localhost', '127.0.0.1', 'antly.fr', 'www.antly.fr']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',  # added for allauth
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'stripe',
    'sslserver',
    'storages',
    'cloudinary',
    'cloudinary_storage',


    'user',
    'sale',
    'super',
    'admin_supplier',

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'LyAnt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LyAnt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'antly-projectdata-base',
        'USER': 'antly-projectuser',
        'PASSWORD': ":)Solenops1s<$o",
        'HOST': '35.205.253.192',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SITE_ID = 1

# media

MEDIA_ROOT = BASE_DIR / "media"
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'he8kyfyn7',
    'API_KEY': '131631381727338',
    'API_SECRET': '582qD-SeI5Ni-oD-2P1fZclls1g',
}
cloudinary.config(**CLOUDINARY_STORAGE)

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# user
AUTH_USER_MODEL = "user.Shopper_m"


# email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'antly.fourmis@gmail.com'
EMAIL_HOST_USER = 'antly.fourmis@gmail.com'
EMAIL_HOST_PASSWORD = 'ckmundpxxmqpkjdm'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# google sheets

API_GOOGLE = "AIzaSyDzfwJz7M-oLbSFZwXoiXLL9kKblo_SSIE"
# cookies

# SESSION_EXPIRE_AT_BR0WSER_CL0SE = True  # cookies delete themselves when the window is closed

# Stripe and Braintree Settings
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

# PayPal
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = 'sandbox'

# company

COMPANY_NAME = "Antly"
COMPANY_ADDRESS = "8 chemin des maraîchers Tresserve 73100"
COMPANY_EMAIL = "antly.fourmis@gmail.com"
COMPANY_PHONE = "06 51 33 61 58"
COMPANY_SIRET = "91493900400018"
COMPANY_VAT_NUMBER = "Pas de TVA applicable"


# offer

FREE_COLONIE = False
FREE_COLONIE2 = False
FREE_COLONIE1 = False
FREE_SHIPPING_COSTE = True

PERCENT_ANTLY = 15

# storage


# Configuration pour utiliser SSL/TLS avec Heroku et Cloudflare (https)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True