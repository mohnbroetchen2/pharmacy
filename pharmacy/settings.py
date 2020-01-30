"""
Django settings for pharmacy project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")
EMAIL_HOST = '127.0.0.1'
# Application definition

#EMAIL_RESPONSIBLE = 'info.huber@aol.de'
#EMAIL_ADMIN = 'info.huber@aol.de'
#DEFAULT_FROM_EMAIL = "bushaltestelle.70@gmail.com"
#EMAIL_HOST = "smtp.gmail.com"
#EMAIL_HOST_USER = "bushaltestelle.70@gmail.com"
#EMAIL_HOST_PASSWORD = ""
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'widget_tweaks',
    'pharmadoc',
    'django_admin_listfilter_dropdown',
    'changelog.apps.ChangelogConfig',
    #'admin_reorder',
    'bulma',
    'django_extensions',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'pharmacy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'pharmacy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

ADMIN_REORDER = (
    {'app': 'pharmadoc', 'label': 'PHARMADOC', 'models': (
        {'model': 'pharmadoc.Pharmacy', 'label': 'Pharmacy'},
        {'model': 'pharmadoc.Order', 'label': 'Order'},
        {'model': 'pharmadoc.Submission', 'label': 'Submissions'},
        {'model': 'pharmadoc.Person', 'label': 'Persons'},
        {'model': 'pharmadoc.Company', 'label': 'Companies'},
        {'model': 'pharmadoc.Vendor', 'label': 'Vendors'},
        {'model': 'pharmadoc.DrugClass', 'label': 'Drug class'},
        {'model': 'pharmadoc.Molecule', 'label': 'Molecule'},
        )},
    {'app': 'auth', 'models': ('auth.User',) },
    {'app': 'changelog', 'label': 'Changelog' },
    'admin_interface',
)

def FILTERS_VERBOSE_LOOKUPS():
    from django_filters.conf import DEFAULTS

    verbose_lookups = DEFAULTS['VERBOSE_LOOKUPS'].copy()
    verbose_lookups.update({
        'icontains': '',
    })
    return verbose_lookups

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

DATETIME_FORMAT = 'd.m.Y H:i:sO'
DATE_FORMAT = 'd.m.Y'
DATE_INPUT_FORMATS =\
[
    '%d.%m.%y', '%d.%m.%Y',
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
]

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


try:
    from .local_settings import *
except ImportError:
    print("Could not import local_settings!")
    pass