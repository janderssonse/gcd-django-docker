from os import environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get('MYSQL_DATABASE'),
        'USER': environ.get('MYSQL_USER'),
        'PASSWORD': environ.get('MYSQL_PASSWORD'),
        'HOST': 'db',
        'PORT': 3306,
        'ATOMIC_REQUESTS': True,
    }
}

SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error', 'models.E025',
                          'fields.W903']

CACHES = {
    'default': {
        'BACKEND': 'apps.middleware.memcached_backend.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.comics.org',
    '.comics.org.',  # Allow FQDN and subdomains.  Can be dropped in 1.7
]

def _modify(settings):
    settings['INSTALLED_APPS'] += ('django_extensions',)

# Search needs Elasticsearch 7.x; start it with
#   docker compose --profile search up -d es
# and set USE_ELASTICSEARCH=1 in the web environment.
if environ.get('USE_ELASTICSEARCH'):
    USE_ELASTICSEARCH = True
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE':
                'apps.gcd.elastic_backend_boosting.Elasticsearch7BoostingSearchEngine',
            'URL': environ.get('ES_URL', 'http://es:9200/'),
            'INDEX_NAME': 'haystack',
            'INCLUDE_SPELLING': True,
        },
    }
