from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class EmailComplete:

	fulfilled = {
		'subject':	'Promise complete. Status: Fulfilled!',
		'intro':	'Congratulations! {otherEmail} has marked your promise as "Fulfilled"',
		'button':	'View Promise',
		'new':		'Click below if you would like to make another promise or send a promise request:',
		'btnNew':	'Make New Promise',
	}
	broken = {
		'subject':	'Promise complete. Status: Broken',
		'intro':	'{otherEmail} has marked your promise as "Fulfilled"',
		'button':	'View Promise',
		'new':		'Click below if you would like to make another promise or send a promise request:',
		'btnNew':	'Make New Promise',
	}

	@classmethod
	def sendEmail(cls, toEmail, otherEmail, url, contentDict):

		fromEmail = 'PromiseTracker<mail@PromiseTracker.com>'

		# set up email message
		plaintext = get_template('EmailComplete.txt')
		html = get_template('EmailComplete.html')

		# fetch class dictionary via string contentDict value
		params = getattr(cls, contentDict)
		params['url'] = url
		subject = params['subject']
		params['intro'] = params['intro'].format(otherEmail=otherEmail)

		textContent = plaintext.render(params)
		htmlContent = html.render(params)
		email = EmailMultiAlternatives(subject, textContent, fromEmail, [toEmail])
		email.attach_alternative(htmlContent, "text/html")

		# send email
		email.send()
