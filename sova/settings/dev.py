from .base import *


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sova',
        'USER': 'sova_user',
        'PASSWORD': 'GoldGate276',
        'HOST': 'localhost',
        'PORT': '5432',
        },
    }

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w$l^g(!s#yq77ex9liinc)qeu^=y#g58-n3thd@l^*^o#$5x39"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# try:
#     from .local import *
# except ImportError:
#     pass
