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
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SHELL_PLUS_DONT_LOAD = [
    "banjo",
]

