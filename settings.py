import os

ADMINS = (
    ('David Krisch', 'david.krisch@billtally.com'),
)

MANAGERS = ADMINS

SITE_ROOT = '/'.join(os.path.dirname(__file__).split('/'))

DEFAULT_FROM_EMAIL='support@billtally.com'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'nke$&&_o2ex=@h92@a1-*r%rz&fzg4)^41prw_n0rpy)7c64m)'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader'
)
 
TEMPLATE_CONTEXT_PROCESSORS = (
		'django.contrib.auth.context_processors.auth',
		'django.core.context_processors.debug',
		'django.core.context_processors.i18n',
		'django.core.context_processors.media',
		'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'billtally.urls'

TEMPLATE_DIRS = (
		'%s/site/templates/' % SITE_ROOT
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'registration',
    'crispy_forms',
    'billtally.site',
    'billtally.api',
]

# django-registration
ACCOUNT_ACTIVATION_DAYS = 5
REGISTRATION_OPEN = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL='/list/'
