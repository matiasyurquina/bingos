import os
from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '%r$bt_tosn%nr^7-9q$-h4tz%_4dqft25v0^m8l(2_4w!db4u('

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bingos',
    'publicidad',
    'admin_manager',
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

ROOT_URLCONF = 'bingos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bingos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bingos',
        'USER' : 'matias',
        'PASSWORD' : '123456',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432',
    	}
}

# DATABASES = {
#  'default': {
#      'ENGINE': 'django.db.backends.mysql',
#      'NAME': 'bingos$bingos',
#      'USER': 'bingos',
#      'PASSWORD': 'G2220HDA',
#      'HOST': 'bingos.mysql.pythonanywhere-services.com',  # Puedes cambiarlo si la base de datos está en otro servidor
#      'PORT': '',       # Puerto por defecto de MySQL
#  }
# }

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
#STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), 'home/bingos/grouped/bingos']
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# LOGIN_REDIRECT_URL = 'login.html'
# LOGOUT_REDIRECT_URL = 'login.html'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')