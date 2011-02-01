from django.db import models
from django.forms import ModelForm, BooleanField
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.rrule import *
from django.forms.models import model_to_dict
from util import get_date_range
import csv

RECURRENCE_FREQ_MAP = {'daily': DAILY, 'weekly': WEEKLY, 'monthly': MONTHLY, 'yearly': YEARLY}
RRULE_WEEKDAY_MAP = {0: MO, 1: TU, 2: WE, 3: TH, 4: FR, 5: SA, 6: SU}
RECURRENCE_WEEKDAY_MAP = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}

class Bill(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	date = models.DateField()
	is_paid = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True)
	
	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
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
	byweekdaycount = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True)
	bill = models.ForeignKey(Bill, editable=False)
	objects = RecurrenceManager()

	def __unicode__(self):
		return "Recurring %s" % self.bill.name

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
		
		start_date, end_date = get_date_range(start_date, end_date)

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
			if key in ['bysetpos', 'bymonth', 'bymonthday', 
										'byyearday', 'byweekno', 'byweekday', 'byweekdaycount']:
				# Convert CommaSeparatedInteger fields into lists of integers
				reader = csv.reader([value.lstrip('[').rstrip(']')])
				model_dict[key]= [int(x) for x in reader.next()]

		# Delete the keys from the list we just made
		for item in to_remove:
			del model_dict[item]

		# Handle the monthly on the second tuesday case
		if 'byweekdaycount' in model_dict:
			weekday = model_dict['byweekday'][0]
			count = model_dict['byweekdaycount'][0]
			model_dict['byweekday'] = RRULE_WEEKDAY_MAP[weekday](count)
			del model_dict['byweekdaycount']

		rrule_obj = rrule(RECURRENCE_FREQ_MAP[self.frequency], **model_dict)

		return rrule_obj.between(start_date, end_date, inc=True) 
	
	class Meta:
		verbose_name = 'recurrence'
		verbose_name_plural = 'recurrence'

