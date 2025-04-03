from .base import *


DEBUG= True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
   
    
}

# Hubicación url para los archivos estaticos
STATIC_URL = 'static/'


# Path de hubicacion para la carpeta static delos archivos estaticos
STATIC_FILES = [BASE_DIR.child('staticfiles')]


# Path de hubicacion para la carpeta static delos archivos estaticos 
# para la variable de configuración STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR.child('staticfiles')]



# python manage.py test --settings=myproject.test_settings


REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'tests': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}