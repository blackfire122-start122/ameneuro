from django import template
from ameneuro.settings import MEDIA_URL
from ..models import AllTheme, def_all_theme
register = template.Library()

@register.filter
def try_url(obj,atrr):
	obj_atrr = getattr(obj,atrr,None)
	if not obj_atrr is None:
		if obj_atrr.name:
			return obj_atrr.url
	return AllTheme.objects.get(pk=def_all_theme()).no_media_img.url