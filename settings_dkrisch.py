from settings import *
import os

def rel(path):
	return os.getcwd() + path

FIXTURE_DIRS = ['fixtures']

STATIC_DOC_ROOT = rel('/site/templates/static')
