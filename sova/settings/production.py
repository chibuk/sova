from .base import *

DEBUG = False

ALLOWED_HOSTS = ["sport-nur.ru", "www.sport-nur.ru", "185.177.219.173"]

DATABASES = {
    "default": {
	"ENGINE": "django.db.backends.postgresql",
	"NAME": "sova",
	"USER": "sovauser",
	"PASSWORD": "GoldGate276",
	"HOST": "127.0.0.1",
	"PORT": "",
    }
}


#try:
#    from .local import *
#except ImportError:
#    pass
