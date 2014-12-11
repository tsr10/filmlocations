from .settings import *

# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'heroku_app32307978',                      # Or path to database file if using sqlite3.
        'USER': 'heroku_app32307978',                      # Not used with sqlite3.
        'PASSWORD': 'ceo3ce73hm8qt33kl17n3msh0u',                  # Not used with sqlite3.
        'HOST': 'ds061200.mongolab.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 61200,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEBUG = False

TEMPLATE_DEBUG = False