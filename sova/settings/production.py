from .base import *

DEBUG = False

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

try:
    from .local import *
except ImportError:
    pass
