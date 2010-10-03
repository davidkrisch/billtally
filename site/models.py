from django.db import models
from django.forms import ModelForm, BooleanField
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.rrule import *
from dateutil.relativedelta import *
from django.forms.models import model_to_dict

FREQUENCY_MAP = {'daily': DAILY, 'weekly': WEEKLY, 'monthly': MONTHLY, 'yearly': YEARLY}

class Bill(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	date = models.DateField()
	is_paid = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True)
	
	def __unicode__(self):
		return self.name

	def get_absolute_url():
		return "/bills/%i/" % self.id
	
	class Meta:
		ordering = ['date']
		verbose_name = 'bill'
		verbose_name_plural = 'bills'

class RecurrenceManager(models.Manager):
	'''Custom manager to deal with Recurrence instances based on rrule objects'''
	pass

class Recurrence(models.Model):
	FREQUENCY_CHOICES = (
	            ('DAILY', DAILY),
	            ('WEEKLY', WEEKLY),
	            ('MONTHLY', MONTHLY),
	            ('YEARLY', YEARLY),
	        )
	frequency = models.CharField(max_length=7, choices=FREQUENCY_CHOICES)
	dtstart = models.DateField()
	interval = models.PositiveIntegerField(null=True, blank=True)
	count = models.IntegerField(null=True, blank=True)
	until = models.DateField(null=True, blank=True)
	bysetpos = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True)
	bymonth = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True)
	bymonthday = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True)
	byyearday = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True) 
	byweekno = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True) 
	byweekday = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True) 
	bill = models.ForeignKey(Bill, editable=False)
	objects = RecurrenceManager()

	def as_list(self, start_date=None, end_date=None):
		'''Retrieve this Recurrence as a list of dates that this recurrence represents
		
			With no arguments, returns the next 30 days by default

			Arguments (datetime objects)
				start_date - (optional) If specified, the rrule will start at this datetime
					If not specified, the start date will be today
				end_date - (optional) If specified, the rrule will end at start_date plus 1 month
					If not specified, the end date will be 30 days from the start date
		'''
		if not self.frequency or not self.dtstart:
			raise Exception('frequency or dtstart not defined')
		
		if not start_date:
			start_date = datetime.today()
		if not end_date:
			end_date = start_date + relativedelta(months=+1)

		# Convert this model to a dictionary
		model_dict = model_to_dict(self, exclude=['id', 'bill'])

		# Remove frequency because it isa positional argument
		del model_dict['frequency']

		# Convert until to a datetime object or remove it if it isn't defined
		if model_dict['until']:
			model_dict['until'] = datetime.strptime(model_dict['until'], '%Y-%m-%d')
		else:
			del model_dict['until']

		# Delete unused keys
		to_remove = []
		for key, value in model_dict.iteritems():
			if not value:
				to_remove.append(key)
		for item in to_remove:
			del model_dict[item]

		# Convert dtstart to a datetime object
		model_dict['dtstart'] = datetime.strptime(model_dict['dtstart'], '%Y-%m-%d')
		rrule_obj = rrule(FREQUENCY_MAP[self.frequency], **model_dict)

		return rrule_obj.between(start_date, end_date, inc=True) 
	
	class Meta:
		verbose_name = 'recurrence'
		verbose_name_plural = 'recurrence'
