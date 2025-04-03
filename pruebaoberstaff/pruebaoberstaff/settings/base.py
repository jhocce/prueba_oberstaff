import os
from unipath import Path


# key con el que se genera el JWT para el token de sesion del usuario 
SECRET_KEY_USER = os.environ.get("SECRET_KEY_USER") 



BASE_DIR = Path(__file__).ancestor(3)

SECRET_KEY = 'django-insecure-gu*x4vx0u$%r5l%7e%kcbc+!v$!ovx_orz0kl^th9q)s$vhr%7'

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]
APPS_LOCAL = [
    'apps.user',
    'apps.system',
    'apps.proyecto',
    
    
]
THY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_yasg',

]
INSTALLED_APPS = DJANGO_APPS + APPS_LOCAL + THY_APPS



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pruebaoberstaff.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'pruebaoberstaff.wsgi.application'

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'es-Ve'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# TEMPLATE_DIRS = [BASE_DIR.child("templates")]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT = BASE_DIR.child('static')

AUTH_USER_MODEL = 'user.user'
AUTH_AUTHENTICATION_TYPE="email"
# CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOWED_ORIGINS = [
   
]
ALGORITM_ENCAP_BACK = "RS256"

# CSRF_TRUSTED_ORIGINS = ['181.208.156.49'] 

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}


