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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
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
		'django.contrib.messages',
		'registration',
		'compress',
    'billtally.site',
    'billtally.api',
)

ACCOUNT_ACTIVATION_DAYS = 5
REGISTRATION_OPEN = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL='/list/'

COMPRESS_CSS = {
		'login_form': {
				'source_filenames': ('css/style.css', 'css/site.css', 'css/forms.css'),
				'output_filename': 'css/login_compressed.css'
			},
		'registration_form': {
				'source_filenames': ('css/style.css', 'css/site.css', 'css/forms.css', 'css/registration.css'),
				'output_filename': 'css/registration_compressed.css'
			},
		'password_reset_enteremail': {
				'source_filenames': ('css/style.css', 'css/site.css', 'css/forms.css', 'css/password-reset-enteremail.css'),
				'output_filename': 'css/password_reset_enteremail_compressed.css'
			},
		'password_reset_form': {
				'source_filenames': ('css/style.css', 'css/site.css', 'css/forms.css', 'css/password-reset-form.css'),
				'output_filename': 'css/password_reset_form_compressed.css'
			},
		'bill_list': {
			'source_filenames': (None,),
			'output_filename': 'css/bill_list.css'
			},
		'add_bill': {
			'source_filenames': ('css/style.css', 'css/site.css', 'css/forms.css', 'css/create_bill.css',),
			'output_filename': 'css/add_edit_bill.css'
			}
}

COMPRESS_JS = {
}
