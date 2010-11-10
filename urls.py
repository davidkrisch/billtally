from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.conf import settings
from billtally.site import views, models
from billtally.site.forms import RegistrationFormEmailIsUserName
from registration.views import register

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('billtally.site.views',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('billtally.api.urls')),

		# Landing Page
		(r'^$', direct_to_template, {'template': 'index.html'}),

		#	Show the create new bill form or POST a new bill
		(r'^create/', views.create_bill),

		# Show the list of bills
		(r'^list/$', views.list_bills),
)

urlpatterns += patterns('',
		(r'^accounts/register/$', register,
				{'form_class': RegistrationFormEmailIsUserName},
				'registration_register'),

		(r'^accounts/', include('registration.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^bt_static/(?P<path>.*)$', 'django.views.static.serve', 
					{'document_root': settings.STATIC_DOC_ROOT}),
    )
