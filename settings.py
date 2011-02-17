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
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'billtally.urls'

TEMPLATE_DIRS = (
		'%s/site/templates/' % SITE_ROOT
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
		'registration',
		'compress',
    'billtally.site',
    'billtally.api',
)

ACCOUNT_ACTIVATION_DAYS = 5
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL='/list/'

COMPRESS_CSS = {
		'login_form': {
				'source_filenames': ('css/style.css', 'css/site.css', 'css/login.css'),
				'output_filename': 'css/login_compressed.css'
			},
		'bill_list': {
			'source_filenames': (None,),
			'output_filename': 'css/bill_list.css'
			},
		'add_bill': {
			'source_filenames': ('css/style.css', 'create_bill.css'),
			'output_filename': 'css/add_edit_bill.css'
			}
}

COMPRESS_JS = {
}
