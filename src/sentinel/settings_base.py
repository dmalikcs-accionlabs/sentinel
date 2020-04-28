# Django settings for sentinel project.
import os
import re

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Deepak Malik', 'dmalikcs@gmail.com'),
)

MANAGERS = ADMINS

IS_AD_AUTHENTICATION = \
    os.path.exists(os.path.join(PROJECT_PATH, '../../deployment/prod/', 'auth_from_ad'))


AZURE_VAULT_URL = os.getenv('AZURE_VAULT_URL')

if AZURE_VAULT_URL:
    from .load_variables import *
else:
    SENTINEL_DATABASE_NAME = os.getenv('SENTINEL_DATABASE_NAME')
    SENTINEL_DATABASE_USERNAME = os.getenv('SENTINEL_DATABASE_USERNAME')
    SENTINEL_DATABASE_PASSWORD = os.getenv('SENTINEL_DATABASE_PASSWORD')
    SENTINEL_DATABASE_HOST = os.getenv('SENTINEL_DATABASE_HOST')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

    AZURE_STORAGE_ACCOUNT = os.getenv('AZURE_STORAGE_ACCOUNT', None)
    AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY', None)
    AZURE_CUSTOM_DOMAIN = os.getenv('AZURE_CUSTOM_DOMAIN', None)

    AZURE_MEDIA_CONTAINER = os.getenv('AZURE_MEDIA_CONTAINER', 'media')

    AZURE_SB_CONN_STRING = os.getenv('AZURE_SB_CONN_STRING', None)
    AZURE_SB_CANCEL_QUEUE = os.getenv('AZURE_SB_CANCEL_QUEUE', None)

    TENANT_ID = os.getenv('TENANT_ID', None)
    CLIENT_ID = os.getenv('CLIENT_ID', None)
    RELYING_PARTY_ID = os.getenv('RELYING_PARTY_ID', None)
    AUDIENCE = os.getenv('AUDIENCE', None)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': SENTINEL_DATABASE_NAME,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': SENTINEL_DATABASE_USERNAME,
        'PASSWORD': SENTINEL_DATABASE_PASSWORD,
        'HOST': SENTINEL_DATABASE_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, '..', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, '..', 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# Production installs need to have this environment variable set
DEFAULT_SECRET_KEY = '$x&j!hodety@6wf@p_xvbvxdh05@%_q^(doptx%mp7v3g-s46&'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', DEFAULT_SECRET_KEY)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, '..', 'templates'),

        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

            ],
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]



MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django_auth_adfs.middleware.LoginRequiredMiddleware',

    # 'sentinel.authentication_middleware.AutomaticUserLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',



    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Uncomment the following if using any of the SSL settings:
)

ROOT_URLCONF = 'sentinel.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sentinel.wsgi.application'


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.postgres',
    'storages',

    #3rd part Application

    'django_extensions',
    'rest_framework',
    'sentinel',
    'users',
    'collector',
    'parsers',
    'destination',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        "json": {
            '()': 'json_log_formatter.JSONFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ.get('LOG_FILE_PATH', '/var/log/sentinel/app.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'werkzeug': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentinel': {
            'level': 'INFO',
            'handlers': ['applogfile',],
            'propagate': True,
        },
        'django_auth_adfs': {
            'handlers': ['console','applogfile'],
            'level': 'DEBUG',
        },

    }
}



IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'/null/?$'),
    re.compile(r'^/phpmyadmin/', re.IGNORECASE),
    re.compile(r'^/favicon\.ico.*$'),
    re.compile(r'^/wp-admin/'),
    re.compile(r'^/cgi-bin/'),
    re.compile(r'^(?!/static/).*\.(css|js)/?$'),
)


# Email configuration
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = ''
#EMAIL_PORT = 465
#EMAIL_HOST_USER = 'webserver@sentinel.com'
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True


INTERNAL_IPS = (
    '192.168.1.151',
    '117.218.42.220',
    '86.6.131.38',
)

AUTH_USER_MODEL = 'users.User'


if AZURE_STORAGE_ACCOUNT \
        and AZURE_ACCOUNT_KEY and AZURE_CUSTOM_DOMAIN:

    DEFAULT_FILE_STORAGE = 'sentinel.custom_azure.AzureMediaStorage'
    # STATICFILES_STORAGE = 'sentinel.custom_azure.AzureStaticStorage'

    MEDIA_LOCATION = "media"
    # STATIC_LOCATION = "static"

    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    # STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'


"""
Azure AD settings
"""

if IS_AD_AUTHENTICATION and TENANT_ID and CLIENT_ID and RELYING_PARTY_ID and AUDIENCE:
    INSTALLED_APPS = ["django_auth_adfs",] + INSTALLED_APPS

    AUTHENTICATION_BACKENDS = [
        # 'django.contrib.auth.backends.ModelBackend',
        'django_auth_adfs.backend.AdfsAuthCodeBackend',
    ]

    AUTH_ADFS = {
        "TENANT_ID": TENANT_ID,
        "CLIENT_ID": CLIENT_ID,
        "RELYING_PARTY_ID": RELYING_PARTY_ID,
        "AUDIENCE": AUDIENCE,
        "CLAIM_MAPPING": {"first_name": "given_name",
                          "last_name": "family_name",
                          "email": "email"},
        "USERNAME_CLAIM": "upn",
        "CREATE_NEW_USERS": True,
        "GROUP_TO_FLAG_MAPPING": {"is_staff": "OPS Automation - Users",
                                  "is_superuser": "OPS Automation - Admin"},

    }
    LOGIN_REDIRECT_URL = "/"
