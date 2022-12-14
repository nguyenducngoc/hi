"""
Django settings for bona_blog project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
from unittest.mock import DEFAULT
import django_heroku
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h((g0d1e)y#zn%d!2wt_ow5otovu5nd#lv7v#_h_o&(m$vtbzc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['shyu1.herokuapp.com','shuyi.online']


# Application definition

INSTALLED_APPS = [

    # Default Django Apps.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps.
    'django_filters',
    'rest_framework',
    'taggit',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    

    # My apps.
    'blog.apps.BlogConfig',
    'cloudinary',

 ]

INTERNAL_IPS = ['127.0.0.1', '::1']

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bona_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bona_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_d131021b19be49a',
        'USER': 'b80525e9219d5f',
        'PASSWORD' : 'b87f9708',
        'HOST' : 'us-cdbr-east-06.cleardb.net',
     
    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

cloudinary.config( 
  cloud_name = "hv3p1pm6a", 
  api_key = "454333541723272", 
  api_secret = "aOpfL5Nhh9yPmrG1Uf5CRXUoCoA" 
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
django_heroku.settings(locals())
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "blog/static"),
]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media files (User uploaded images)
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Specifies the CSS Framework Crispy Forms should use.heroku git:remote -a shuy1
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Account Settings
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/author/dashboard/'
LOGOUT_REDIRECT_URL = '/account/logout/'

# Email Settings (Development)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Email Settings (Production)

#EMAIL_HOST = 'smtp.sendgrid.net'
#EMAIL_HOST_USER = 'apikey'
#EMAIL_HOST_PASSWORD = "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"
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#MAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# CKEditor Settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default':
        {'toolbar': 'full',
         'width': 'auto',
         'extraPlugins': ','.join([
             'codesnippet',
             'youtube'
         ]),
         },
}