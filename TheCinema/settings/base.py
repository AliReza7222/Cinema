"""
Django settings for TheCinema project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import environ
import os
from datetime import timedelta
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# APi Key KavehNegar and Phone Number
APIKEY = env('APIKEY')
PHONE_NUMBER = env('PHONE_NUMBER')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []

# Config Custom Model User
AUTH_USER_MODEL = "accounts.UserSite"

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular'
]
LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'movie.apps.MovieConfig',
    'payment.apps.PaymentConfig'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env('REDIS_URL'),
    }
}

# config Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# config Simple Jwt for authentication user
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=48),
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=24),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(hours=48),
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS384",

}

# drf_spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Cinema API",
    "DESCRIPTION": "Documentation of API endpoints of Cinema",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r'/api/v[0-9]',
    'SERVE_INCLUDE_SCHEMA': False,
    # "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
}

ROOT_URLCONF = 'TheCinema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = 'TheCinema.wsgi.application'

# config corsheaders
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000", # project Django
    "http://localhost:3000", # project React
]


# csrf origin
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000", # project React
]

# security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Config DataBase on Postgresql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('NAME_DATABASE'),
        'USER': env('USER_DATABASE'),
        'PASSWORD': env('PASSWORD_DATABASE'),
        'HOST': env('HOST_DATABASE'),
        'PORT': env('PORT_DATABASE')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'


# Media files

MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
