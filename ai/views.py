from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .tasks import recognize_task
import binascii
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from PIL import Image

class recognize(LoginRequiredMixin,TemplateView):
	template_name = "ai/recognize.html"
	login_url = 'login'

@login_required(login_url='login')
def form_recognize_ajax(request):
	img = binascii.b2a_base64(request.FILES["img"].__dict__["file"].read())
	recognize_task.delay(img=img.decode('utf8'),username=request.user.username)
	return JsonResponse({"data":"on recognize"})