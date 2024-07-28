import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from drf_yasg import openapi

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True if os.environ.get("DEBUG") == "True" else False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'djoser',
    'drf_yasg',

    'handlerapi',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT", 5432),
    }
}

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_FILTERS = [
    'ad_title',
    'ad_id',
    'ad_author',
    'ad_views',
    'ad_position'
]

PARAMS_TO_CONVENT = [
    'ad_views',
    'ad_id',
    'ad_position',
    'ad_author'
]

MANUAL_PARAMETERS = [openapi.Parameter('ad_title',
                                       openapi.IN_QUERY,
                                       description="Заголовок объявления",
                                       type=openapi.TYPE_STRING),
                     openapi.Parameter('ad_id',
                                       openapi.IN_QUERY,
                                       description="id объявления",
                                       type=openapi.TYPE_INTEGER),
                     openapi.Parameter('ad_author',
                                       openapi.IN_QUERY,
                                       description="Автор объявления",
                                       type=openapi.TYPE_INTEGER),
                     openapi.Parameter('ad_views',
                                       openapi.IN_QUERY,
                                       description="Количество просмотров объявления",
                                       type=openapi.TYPE_INTEGER),
                     openapi.Parameter('ad_position',
                                       openapi.IN_QUERY,
                                       description="Позиция объявления",
                                       type=openapi.TYPE_INTEGER),
                     ]

PROPERTIES = {
    'ad_title': openapi.Schema(type=openapi.TYPE_STRING, description="Заголовок объявления"),
    'ad_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id объявления"),
    'ad_author': openapi.Schema(type=openapi.TYPE_STRING, description="Автор объявления (Название автора строчкой)"),
    'ad_views': openapi.Schema(type=openapi.TYPE_INTEGER, description="Количество просмотров объявления"),
    'ad_position': openapi.Schema(type=openapi.TYPE_INTEGER, description="Позиция объявления"),
}

AUTHORIZATION = [
    openapi.Parameter('Authorization',
                      in_=openapi.IN_HEADER,
                      description="JWT токен",
                      type=openapi.TYPE_STRING,
                      required=True, )
]
