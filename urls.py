from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib.auth.views import login as auth_login
from billtally.site import views, models
from billtally.site.forms import RegistrationFormEmailIsUserName
from registration.views import register, activate

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('billtally.site.views',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #(r'^api/', include('billtally.api.urls')),

		# Landing Page
		(r'^$', direct_to_template, {'template': 'index.html'}),

		#	Show the create new bill form or POST a new bill
		url(r'^create/', views.create_edit_bill, {'bill_id': None}, name='create_bill'),

		#	Show the edit bill form or POST a new bill
		url(r'^edit/(?P<bill_id>\d+)/$', views.create_edit_bill, name='edit_bill'),

		#	Show the edit bill form or POST a new bill
		url(r'^delete/(?P<bill_id>\d+)/$', views.delete_bill, name='delete_bill'),

		# Show the list of bills
		url(r'^list/$', views.list_bills, name='list_bills'),

		#	Mark a bill as paid
		url(r'^paid/(?P<bill_id>\d+)/$', views.mark_bill_paid, name='mark_bill_paid'),

		# Self serve account admin page
		(r'^myaccount/', direct_to_template, {'template': 'myaccount.html'}, 'myaccount'),
)

urlpatterns += patterns('',
		(r'^accounts/register/$', register,
				{'form_class': RegistrationFormEmailIsUserName,
				 'backend': 'registration.backends.default.DefaultBackend'},
				'registration_register'),

		(r'^accounts/activate/(?P<activation_key>\w+)/$', activate,
				{'backend': 'registration.backends.default.DefaultBackend',
				 'success_url': settings.LOGIN_REDIRECT_URL},
				'registration_activate'),

		(r'^accounts/', include('registration.backends.default.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^bt_static/(?P<path>.*)$', 'django.views.static.serve', 
					{'document_root': settings.STATIC_DOC_ROOT}),
    )
