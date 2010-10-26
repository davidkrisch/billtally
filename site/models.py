from django.db import models
from django.forms import ModelForm, BooleanField
from django.contrib.auth.models import User
from datetime import datetime
from datetime import time
from dateutil.rrule import *
from dateutil.relativedelta import *
from django.forms.models import model_to_dict

RECURRENCE_FREQ_MAP = {'daily': DAILY, 'weekly': WEEKLY, 'monthly': MONTHLY, 'yearly': YEARLY}

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
	            ('DAILY', 'daily'),
	            ('WEEKLY', 'weekly'),
	            ('MONTHLY', 'monthly'),
	            ('YEARLY', 'yearly'),
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
				start_date - (optional) datetime object - if specified, the rrule will start at this datetime
					If not specified, the start date will be today
				end_date - (optional) datetime object - if specified, the rrule will end at start_date plus 1 month
					If not specified, the end date will be 30 days from the start date
			Returns
				list of the dates that this recurrence represents
		'''
		if not self.frequency or not self.dtstart:
			raise Exception('frequency or dtstart not defined')
		
		if not start_date:
			start_date = datetime.today()
		if not end_date:
			end_date = start_date + relativedelta(months=+1)
			end_date = datetime.combine(end_date, time())

		# Convert this model to a dictionary
		model_dict = model_to_dict(self, exclude=['id', 'bill'])

		# Remove frequency because it is a positional argument
		del model_dict['frequency']

		# Find keys that are blank so we can remove them 
		to_remove = []
		for key, value in model_dict.iteritems():
			if not value:
				to_remove.append(key)
				continue
			if key in ['bysetpos', 'bymonth', 'bymonthday', 'byyearday', 'byweekno', 'byweekday']:
				# Convert CommaSeparatedInteger fields into lists of integers
				model_dict[key] = [int(x) for x in value]

		# Delete the keys from the list we just made
		for item in to_remove:
			del model_dict[item]

		rrule_obj = rrule(RECURRENCE_FREQ_MAP[self.frequency], **model_dict)

		return rrule_obj.between(start_date, end_date, inc=True) 
	
	class Meta:
		verbose_name = 'recurrence'
		verbose_name_plural = 'recurrence'
