"""
Django settings for iasf project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

try:
    from .secret import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, SENDGRID_API_KEY
    SETTING_DEBUG = True
    SETTING_SSL_REQUIRE = False
except ImportError:
    DB_NAME = ""
    DB_KEY = ""
    AZURE_ACCOUNT_NAME = ""
    AZURE_ACCOUNT_KEY = ""
    SENDGRID_API_KEY = ""
    SETTING_DEBUG = False
    SETTING_SSL_REQUIRE = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRETKEY','ecapu-9949l%m7_!$c65_*fi1b(t)$v4absi8=j6#4z!t$fu$9')

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get("DEBUG") == "TRUE" or SETTING_DEBUG==True :
    DEBUG = True
else:
    DEBUG = False

print("Debug mode is " + "True" if SETTING_DEBUG else "False")

ALLOWED_HOSTS = ['iasfapply-staging.azurewebsites.net', 'iasfapply.azurewebsites.net', 'iasfapplynew-staging.azurewebsites.net', 'iasfapplynew.azurewebsites.net', 'apply.iasf.org', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'constrainedfilefield',
    'betterforms',
    'iasf.accounts',
    'iasf.apply',
    'iasf.review',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iasf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'iasf/templates')],
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

WSGI_APPLICATION = 'iasf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('DATABASENAME', 'iasf'),
        'USER': os.environ.get('DATABASEUSER', 'test'),
        'PASSWORD': os.environ.get('DATABASEPASSWORD', 'test'),
        'HOST': os.environ.get('DATABASEHOST', 'localhost'),
        'PORT': os.environ.get('DATABASEPORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require' if SETTING_SSL_REQUIRE else 'disable',
        }
    },
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'iasf/static')
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_REDIRECT_URL = '/apply'
LOGOUT_REDIRECT_URL = '/apply'

DEFAULT_FILE_STORAGE = 'iasf.common.storages.AzureStorage'
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', AZURE_ACCOUNT_NAME)
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', AZURE_ACCOUNT_KEY)
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'applicationfiles')

# Magic file path -- used for file type validation.
MAGIC_FILE_PATH = os.path.join(BASE_DIR, 'bin\magic.mgc')

# Email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", SENDGRID_API_KEY)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 14

DEFAULT_FROM_EMAIL = "info@iasf.org"