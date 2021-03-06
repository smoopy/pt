from django import forms
from django.contrib.admin import widgets
#from datetime import datetime

from classes.encryption import Encryption
from prom.models import blacklist



class promiseForm(forms.Form):

	def clean(self):
		cleaned_data = super(promiseForm, self).clean()
		emailpromor = cleaned_data.get('emailpromor')
		emailpromee = cleaned_data.get('emailpromee')

		if emailpromor == None or emailpromee == None:
			raise forms.ValidationError('Email addresses must be valid.')

		emailpromor = emailpromor.lower()
		emailpromee = emailpromee.lower()

		if emailpromor and emailpromee and (emailpromor == emailpromee):
			#self._errors['emailpromee'] = self.error_class(['Emails cannot be the same.'])
			#del self.cleaned_data['emailpromee']
			raise forms.ValidationError('Emails must be different.')

		if isBlacklisted(emailpromor):
			raise forms.ValidationError(emailpromor + ' is blacklisted.')
		if isBlacklisted(emailpromee):
			raise forms.ValidationError(emailpromee + ' is blacklisted.')

		# LOWERCASE email addresses before going back to view
		cleaned_data["emailpromor"] = emailpromor
		cleaned_data["emailpromee"] = emailpromee

		return cleaned_data

class promorForm(promiseForm):

	PROMISETEXT = (
		'I, [your name], promise I will go to the movies '
		'with Anya on Friday night.'
	)

	emailpromor = forms.EmailField(
		required=True,
		label="Your email",
		# widget=forms.TextInput(attrs={'size':10, 'max_length':20}),
	)

	emailpromee = forms.EmailField(
		required=True,
		label="Promisee email",
	)

	public = forms.BooleanField(
		label="&nbsp;Public",
		required=False,
		widget=forms.CheckboxInput(attrs={
		}),
	)

	details = forms.CharField(
		required=True,
		widget=forms.Textarea(attrs={
			'rows':3,
			'placeholder': PROMISETEXT,
		}),
		max_length=2000,
		label="Promise details",
	)


class promeeForm(promiseForm):

	PROMISETEXT = (
		'I, [name of promisor], promise to pay Kevin '
		'the money I owe him by this Saturday.'
	)

	emailpromee = forms.EmailField(
		required=True,
		label="Your email",
	)

	emailpromor = forms.EmailField(
		required=True,
		label="Promisor email",
	)

	public = forms.BooleanField(
		label="&nbsp;Public",
		required=False,
		widget=forms.CheckboxInput(attrs={
		}),
	)

	details = forms.CharField(
		required=True,
		widget=forms.Textarea(attrs={
			'rows':3,
			'placeholder': PROMISETEXT,
		}),
		max_length=2000,
		label="Promise details",
	)


#####################################################################
# Check if email has been blacklisted
#####################################################################
def isBlacklisted(email):
	encemail = Encryption.encrypt(email)
	Blacklist = blacklist.objects.filter(email=encemail).first()

	if Blacklist:
		return True
	else:
		return False

