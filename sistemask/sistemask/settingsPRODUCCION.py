"""
Django settings for sistemask project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os



BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h1t#p+ll3t6=3y5j*7f=-39(o2qu^orrdx%1m1k!kctcu=zmr='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adm_usuarios',
    'adm_roles',
    'adm_proyectos',
    'adm_flujos',
    'adm_sprints',
    'adm_historias',
    'adm_actividades',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sistemask.urls'

WSGI_APPLICATION = 'sistemask.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME':'sistemask',
	    'USER': 'postgres',
	    'PASSWORD':'postgres',
	    'HOST': '127.0.0.1',
	    'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = '/var/www/sistemask/'
MEDIA_URL = 'http://127.0.0.1:80/historia/tareas/'

STATIC_URL = 'http://sistemask.com/static/'


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

LOGIN_URL = '/'
LOGOUT_URL = '/salir'
LOGIN_REDIRECT_URL = '/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sistemaskmail@gmail.com'
EMAIL_HOST_PASSWORD = 'sistemask'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PATH = '/var/www/sistemask'
