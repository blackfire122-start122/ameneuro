from django import template

register = template.Library()

@register.filter
def split_mess(val,string):
	return val.split(string)

