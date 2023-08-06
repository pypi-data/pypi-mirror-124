from os.path import abspath, dirname, join

BASE_DIR = dirname(abspath(__file__))
DEBUG=False
ROOT_URLCONF = "banjo.urls"
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.sqlite',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ALLOWED_HOSTS = "*"
SECRET_KEY = "xxx"
INSTALLED_APPS = [
    "django_extensions",
    "banjo",
    "app",
]
SHELL_PLUS_DONT_LOAD = [
    "banjo",
]

