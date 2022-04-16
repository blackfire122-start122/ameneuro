from django import template

register = template.Library()

@register.filter
def url_from_options(th,opt):
	return getattr(th,opt)

