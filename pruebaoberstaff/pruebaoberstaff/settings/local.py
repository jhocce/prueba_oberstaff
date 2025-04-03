from .base import *
DEBUG= True
ALLOWED_HOSTS = ['*', "localhost"]






DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    # 'mongodb': {
    #     'URI': 'mongodb://localhost:27017',
    #     'NAME': 'casino',
    # }
    
}

# Hubicación url para los archivos estáticos
STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR.child('staticfiles')
# STATIC_ROOT = "/code/static/"


# Path de ubicación para la carpeta static delos archivos estáticos
STATIC_FILES = [BASE_DIR.child('staticfiles')]


# Path de hubicacion para la carpeta static delos archivos estáticos 
# para la variable de configuración STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR.child('staticfiles')]
