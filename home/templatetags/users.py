from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def define(context, name, val=None):
	context[name] = val
	return ""

@register.filter
def filter_ch(query,user):
	if query.filter(chat_friend__user=user):
		return False
	return True

