from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
        'default':
                {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(SITE_ROOT, 'db/billtally.db'),
                }
}

FIXTURE_DIRS = ['fixtures']

STATIC_DOC_ROOT = '%s/site/templates/static' % SITE_ROOT

MEDIA_ROOT = STATIC_DOC_ROOT
MEDIA_URL = '/bt_static/'

MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.append('debug_toolbar')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False 
}
