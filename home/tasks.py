from ameneuro.celery import app
from ameneuro.settings import domain, email_server
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from home.models import User
import logging

logger = logging.getLogger(__name__)

@app.task
def send_email(data):
	associated_users = User.objects.filter(Q(email=data))
	if associated_users.exists():
		for user in associated_users:
			subject = "Password Reset Requested"
			email_template_name = "home/password_reset/password_reset_email.txt"
			c = {
			"email":user.email,
			'domain':domain,
			'site_name': 'Ameneuro',
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user,
			'token': default_token_generator.make_token(user),
			'protocol': 'http',
			}
			email = render_to_string(email_template_name, c)
			try:
				send_mail(subject, email, email_server , [user.email], fail_silently=False)
			except BadHeaderError as e:
				logger.warning(str(e))
				return "Fail"
	return "Good"