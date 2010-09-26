from django.db import models
from django.forms import ModelForm, BooleanField
from django.contrib.auth.models import User

class Recurrence(models.Model):
	FREQUENCY_CHOICES = (
	            ('DAILY', 'daily'),
	            ('WEEKLY', 'weekly'),
	            ('MONTHLY', 'monthly'),
	            ('YEARLY', 'yearly'),
	        )
	frequency = models.CharField(max_length=7, choices=FREQUENCY_CHOICES)
	dtstart = models.DateField()
	interval = models.PositiveIntegerField()
	count = models.IntegerField()
	until = models.DateField()
	bysetpos = models.CommaSeparatedIntegerField(max_length=128)
	bymonth = models.CommaSeparatedIntegerField(max_length=128)
	bymonthday = models.CommaSeparatedIntegerField(max_length=128)
	byyearday = models.CommaSeparatedIntegerField(max_length=128) 
	byweekno = models.CommaSeparatedIntegerField(max_length=128) 
	byweekday = models.CommaSeparatedIntegerField(max_length=128) 

	class Meta:
		verbose_name = 'recurrance'
		verbose_name_plural = 'recurrance'

class Bill(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	date = models.DateField()
	is_paid = models.BooleanField(default=False)
	recurrence = models.ForeignKey(Recurrence, blank=True, null=True)
	
	def __unicode__(self):
		return self.name

	def get_absolute_url():
		return "/bills/%i/" % self.id
	
	class Meta:
		ordering = ['date']
		verbose_name = 'bill'
		verbose_name_plural = 'bills'

class BillForm(ModelForm):
	is_recurring = BooleanField(required=False)
	class Meta:
		model = Bill
		exclude = ('user',)

