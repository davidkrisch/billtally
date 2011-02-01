from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from models import Bill, Recurrence, RECURRENCE_WEEKDAY_MAP
from registration.models import RegistrationProfile
from dateutil.rrule import *

class DateRangeForm(forms.Form):
	"""Form for start and end dates"""
	start = forms.DateTimeField(required=False)
	end = forms.DateTimeField(required=False)

class BillForm(forms.ModelForm):
	"""Form for Bill objects"""
	does_repeat = forms.BooleanField(label='Repeat...', required=False)
	class Meta:
		model = Bill
		exclude = ('user', 'parent')

class RecurrenceForm(forms.Form):
	"""Form for Recurrence objects"""
	repeat_choices = (('daily', 'Daily'), ('weekly', 'Weekly'), 
										('monthly', 'Monthly'), ('yearly', 'Yearly'))
	repeat_every_choices = (('1', 1),('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
													('7', 7),('8', 8), ('9', 9), ('10', 10), ('11', 11), ('12', 12),
													('13', 13),('14', 14), ('15', 15), ('16', 16), ('17', 17), ('18', 18),
													('19', 19),('20', 20), ('21', 21), ('22', 22), ('23', 23), ('24', 24),
													('25', 25),('26', 26), ('27', 27), ('28', 28), ('29', 29), ('30', 30))
	weekday_choices = ((SU, 'Sunday'), (MO, 'Monday'), (TU, 'Tuesday'), (WE, 'Wednesday'), 
											(TH, 'Thursday'), (FR, 'Friday'), (SA, 'Saturday'))
	repeat_by_choices = (('day_of_month', 'day of the Month'), ('day_of_week', 'day of the week'))
	ends_on_choices = (('never', 'Never'), ('until', 'Until'))
	
	repeats = forms.ChoiceField(choices=repeat_choices)
	repeat_every = forms.ChoiceField(choices=repeat_every_choices)
	# Only used for weekly
	repeat_on = forms.MultipleChoiceField(choices=weekday_choices, required=False)
	# Only used for monthly
	repeat_by = forms.ChoiceField(widget=forms.RadioSelect(),
																choices=repeat_by_choices, required=False)
	has_end =  forms.ChoiceField(widget=forms.RadioSelect(),
																choices=ends_on_choices)
	end_date = forms.DateField(required=False)

	def clean_repeat_on(self):
		"""Turn repeat_on into an array of integers (rrule weekdays objects)"""
		repeat_on = self.cleaned_data['repeat_on']
		days = [RECURRENCE_WEEKDAY_MAP[day] for day in repeat_on]
		self.cleaned_data['repeat_on'] = days
		return days 

	def clean(self):
		"""Make sure repeat_by is only set if repeats is monthly
			Make sure repeat on is only set if repeats is weekly
		"""
		cleaned_data = self.cleaned_data
		repeats = cleaned_data.get('repeats')
		repeat_on = cleaned_data.get('repeat_on')
		repeat_by = cleaned_data.get('repeat_by')

		if repeats == 'monthly' and repeat_by == '':
			raise forms.ValidationError("'Repeat by' must be set when creating a bill that repeats monthly")
		elif repeats == 'weekly' and repeat_on == '':
			raise forms.ValidationError("'Repeat on' must be set when creating a bill that repeats weekly")

		return cleaned_data

class RegistrationFormEmailIsUserName(forms.Form):
	"""
		RegistrationForm subclass that uses email address as the username
		and enforces uniqueness of the email address in the system.
	"""
	email = forms.EmailField(max_length=75, label=_(u'email address'))
	password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
								label=_(u'password'))
	password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
								label=_(u'password (again)'))

	def clean_email(self):
		"""Validate that the supplied email address is unique for the site."""
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
		return self.cleaned_data['email']

	def clean(self):
		"""
			Verifiy that the values entered into the two password fields
			match. Note that an error here will end up in
			``non_field_errors()`` because it doesn't apply to a single
			field.
		"""
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_(u'You must type the same password each time'))
		return self.cleaned_data

	def save(self, profile_callback=None):
		"""
			Create the new ``User`` and ``RegistrationProfile``, and
			returns the ``User``.

			This is essentially a light wrapper around
			``RegistrationProfile.objects.create_inactive_user()``,
			feeding it the form data and a profile callback (see the
			documentation on ``create_inactive_user()`` for details) if
			supplied.
		"""
		new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['email'],
				password=self.cleaned_data['password1'], email=self.cleaned_data['email'], profile_callback=profile_callback)
		return new_user
