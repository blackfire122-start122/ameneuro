from django import template
from ameneuro.settings import MEDIA_URL
register = template.Library()

@register.filter
def url_from_options(th,opt):
	return MEDIA_URL + str(getattr(th,opt))

