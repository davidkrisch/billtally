from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from registration.models import RegistrationProfile


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
