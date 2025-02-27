from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # third party app
    'accounts',
    'note',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third party middlewares
    'accounts.middlewares.TokenExpirationMiddleware', # check token expiration
    'accounts.middlewares.LoginRateLimitationMiddleware', # login limitation
    'note.middlewares.security.SecurityMiddleware', # scurity must running very fast
    'note.middlewares.cross_origin_resource_sharing.CrosMiddleware', 
    'note.middlewares.rate_limiting.RateLimitingMiddleware', # limitation of all request
    'note.middlewares.cache.CacheMiddleware', # cache the data
    'note.middlewares.custom_header.CustomHeaderMiddleware', # add custom headers
    'note.middlewares.error_handling.ErrorHandlingMiddleware', # check the error and handle
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


AUTH_USER_MODEL = 'accounts.CustomUser'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'HOST':config('DB_HOST'),
        'USER':config('DB_USER'),
        'PASSWORD':config('DB_PASSWORD'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# LOG SETTINGS
LOGGING = {
    'version':1,
    "disable_existing_loggers":False,
    "formatters": {
        'verbose': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './core/logs/debug.log',
            'formatter': 'verbose'
        },
        'info_file':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './core/logs/info.log',
            'formatter': 'verbose'
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': './core/logs/warning.log',
            'formatter': 'verbose'
        }
    },
    'loggers':{
        'django':{
            'handlers': ['debug_file','info_file','warning_file'],
            'level': 'DEBUG',
            'propagate':True
        },
        'custom_logger':{
            'handlers': ['debug_file','info_file','warning_file'],
            'level':'DEBUG',
            'propagate':False
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
