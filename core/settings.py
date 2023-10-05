"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import json
from datetime import timedelta

import environ

from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environnement variables
env = environ.Env(
    ALLOWED_HOSTS=(
        list,
        [
            "*",
        ],
    ),
    DATABASE_URL=(str, "db1.sqlite3"),
    TWILIO_ACCOUNT_SID=(str, ""),
    TWILIO_AUTH_TOKEN=(str, ""),
    TWILIO_SERVICE=(str, ""),
    BANKILY_ENDPOINT=(str, ""),
    BANKILY_CLIENT_ID=(str, ""),
    BANKILY_USERNAME=(str, ""),
    BANKILY_PASSWORD=(str, ""),
    DEBUG=(bool, False),
    SENTRY_DSN=(str, None),
    SENTRY_TRACES_SAMPLE_RATE=(float, 0.0),
    SENTRY_PROFILES_SAMPLE_RATE=(float, 0.0),
    SENTRY_ENVIRONMENT=(str, "local"),
    CI_BUILD_REF_SLUG=(str, "latest"),
    CI_COMMIT_SHA=(str, "latest"),
)

env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(w^-!6)89)aq^l7@*dv8x=nn$m$@_r-qov^o3ae0mvi)7i-ex&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", env("DEBUG"))

ALLOWED_HOSTS = json.loads(os.getenv("ALLOWED_HOSTS", env("ALLOWED_HOSTS")))

# TWILIO SETTINGS
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", env("TWILIO_ACCOUNT_SID"))
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", env("TWILIO_AUTH_TOKEN"))
TWILIO_SERVICE = os.getenv("TWILIO_SERVICE", env("TWILIO_SERVICE"))

# BANKILY SETTINGS
BANKILY_ENDPOINT = os.getenv("BANKILY_ENDPOINT", env("BANKILY_ENDPOINT"))
BANKILY_CLIENT_ID = os.getenv("BANKILY_CLIENT_ID", env("BANKILY_CLIENT_ID"))
BANKILY_USERNAME = os.getenv("BANKILY_USERNAME", env("BANKILY_USERNAME"))
BANKILY_PASSWORD = os.getenv("BANKILY_PASSWORD", env("BANKILY_PASSWORD"))

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "graphene_graphiql_explorer",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# GRAPHENE SETTINGS
GRAPHENE = {
    "SCHEMA": "core.schema.schema",
    "SCHEMA_OUTPUT": "schema.graphql",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
    ],
    "RELAY_CONNECTION_MAX_LIMIT": 500,
}

# GRAPHQL_JWT SETTINGS
GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=60),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(minutes=60),
    "JWT_ALLOW_ARGUMENT": True,
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "{levelname}; {asctime}; {pathname}; {module}; {lineno}; {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "level": "ERROR",
            "handlers": ["console"],
            "formatter": "verbose",
        },
        "api": {"level": "DEBUG", "handlers": ["console"], "propagande": False},
    },
}
JAZZMIN_SETTINGS = {
    "site_header": "Arena",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to Arena Five",
    # Copyright on the footer
    "copyright": "Arena SARL",
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        {
            "name": "Support",
            "url": "https://site.arenafive.app/support.html",
            "new_window": True,
        },
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
    ],
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "api.arena": "fas fa-home",
        "api.adress": "fas fa-map-marker-alt",
        "api.arenafivesettings": "fas fa-cogs",
        "api.availability": "fas fa-calendar-alt",
        "api.game": "fas fa-futbol",
        "api.manager": "fas fa-users",
        "api.media": "fas fa-photo-video",
        "api.player": "fas fa-user-friends",
        "api.payment": "fas fad fa-credit-card",
        "api.paymentgame": "fas fad fa-credit-card",
        "api.bankilypayment": "fas fa-money-check-alt",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas far fa-key",
    "default_icon_children": "fas fa-key",
}

# SENTRY CONFIGURATION
CI_COMMIT_SHA = env("CI_COMMIT_SHA")
CI_BUILD_REF_SLUG = env("CI_BUILD_REF_SLUG")
VERSION = f"{CI_BUILD_REF_SLUG}-{CI_COMMIT_SHA}"
sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    environment=env("SENTRY_ENVIRONMENT"),
    integrations=[DjangoIntegration()],
    #ca_certs=env("REQUESTS_CA_BUNDLE"),
    attach_stacktrace=True,
    release=VERSION,
    traces_sample_rate=env("SENTRY_TRACES_SAMPLE_RATE"),
    profiles_sample_rate=env("SENTRY_PROFILES_SAMPLE_RATE"),
)

MODELTRANSLATION_LANGUAGES = ("fr", "ar")
MODELTRANSLATION_DEFAULT_LANGUAGE = "fr"
