from django.conf.urls.defaults import *
from piston.resource import Resource
from billtally.api.handlers import BillHandler

bill_handler = Resource(BillHandler)

urlpatterns = patterns('',
				# PUT (update) and DELETE
				url(r'bills/(?P<bill_id>[^/]+)/$', bill_handler),
				# GET (read) and POST (create)
        url(r'bills$', bill_handler),
    )
