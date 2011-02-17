from settings import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

def rel(path):
	return os.getcwd() + path

FIXTURE_DIRS = ['fixtures']

STATIC_DOC_ROOT = rel('/site/templates/static')

MEDIA_ROOT = STATIC_DOC_ROOT
MEDIA_URL = '/bt_static/'
