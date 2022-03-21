from django.shortcuts import render, redirect
from .models import User,Post,Chat,Comment,Theme,TypeMes,Playlist
from .forms import ThemeForm,MessageForm,AllTheme
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from ameneuro.settings import get_posts_how, get_mes_how, get_user_how
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .services import *

from django.core import serializers

# in all need defence

@login_required(login_url='login')
def comment_ajax(request):
	if not request.GET["id"].isdigit():return HttpResponseBadRequest()

	try:post = Post.objects.get(pk=request.GET["id"])
	except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/comments.html",{"post_id":post.id ,"comments":post.comments.all()})

def post_ajax(request):
	posts = {}
	if request.GET["id"]:
		if not request.GET["id"].isdigit():return HttpResponseBadRequest()
		try:posts = Post.objects.filter(pk=request.GET["id"])
		except: HttpResponseNotFound()
	else:posts = get_posts(request,request.user)

	if not posts:return HttpResponse("None post", status=200)
	return render(request, "home/ajax_html/posts.html",{"posts":posts,"type":request.GET.get("type")})

@login_required(login_url='login')
def chat_options_ajax(request):
	chat = {}
	if not request.GET["chat_id"].isdigit():return HttpResponseBadRequest()

	try:chat = Chat.objects.get(pk=request.GET['chat_id'])
	except:return HttpResponseNotFound()

	if not request.user in chat.users.all():return HttpResponseForbidden()

	form = ThemeForm()

	return render(request, "home/ajax_html/chat_options.html",{
			"chat":chat,
			"form":form
		})

@login_required(login_url='login')
def chat_get_mess_ajax(request):
	if not request.GET["chat_id"].isdigit():return HttpResponseBadRequest()
	mess = []

	try:chat = Chat.objects.get(pk=request.GET['chat_id'])
	except:return HttpResponseNotFound()

	if not request.user in chat.users.all():return HttpResponseForbidden()
	mess = list(chat.messages.order_by('-date')[request.session['end_mes_wath']:request.session['end_mes_wath']+get_mes_how][::-1])

	request.session['end_mes_wath'] += get_mes_how
	return render(request, "home/ajax_html/mess.html",{"mess":mess})

@login_required(login_url='login')
def send_file_mes_ajax(request):
	form = MessageForm()
	error = ""

	if request.method == "POST":
		if not request.POST["chat_id"].isdigit():return HttpResponseBadRequest()

		src = ""
		form = MessageForm(request.POST, request.FILES)
		if form.is_valid():
			mes = form.save()
			if not mes.file:return HttpResponseBadRequest()
			mes.user = request.user
			mes.type_m = TypeMes.objects.get(type_m="file")
			mes.save()
			src = "/stream_mess/"+str(mes.id)
			chat = Chat.objects.get(pk=request.POST["chat_id"])
			chat.messages.add(mes)
		else:return HttpResponseBadRequest()
		return JsonResponse({"data_text":"OK","src":src,"type_file":mes.type_file.type_f,"id":mes.id}, status=200)

	return render(request,"home/ajax_html/send_file.html",{"form":form})

@login_required(login_url='login')
def musics_all_ajax(request):
	if request.GET["type"] == "music_share":mus = request.user.music_shared
	elif request.GET["type"] == "playlist":
		try:mus = Playlist.objects.get(name=request.GET["ps"]).musics
		except:return HttpResponseNotFound()
	elif request.GET["type"] == "user_music_add":
		try:mus = User.objects.get(pk=request.GET["id"]).music
		except:return HttpResponseNotFound()
	else:mus = request.user.music
	return render(request,"home/ajax_html/all_music.html",{"music":mus,'type':request.GET["type"]})

@login_required(login_url='login')
def user_find_ajax(request):
	if not request.GET["users_find_start"].isdigit() or not request.GET["users_find_end"].isdigit():return HttpResponseBadRequest()
	users = []
	if request.GET["type"] == "all":
		try:
			if int(request.GET["users_find_end"])-int(request.GET["users_find_start"])!=20:return HttpResponse('Payload Too Large', status=413)
			users = User.objects.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]
		except:return HttpResponseNotFound()
	elif request.GET["type"] == "friends_and_want":
		try:
			if int(request.GET["users_find_end"])-int(request.GET["users_find_start"])!=20:return HttpResponse('Payload Too Large', status=413)
			users = request.user.friend_want_add.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]

			if users.count()<20:
				users |= request.user.friends.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]

		except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/users.html",{"users":users,"type":request.GET["type"]})

@login_required(login_url='login')
def users_get_ajax(request):
	if not request.GET["users_start"].isdigit() or not request.GET["users_end"].isdigit():return HttpResponseBadRequest()
	if int(request.GET["users_start"])-int(request.GET["users_end"])!=-20:return HttpResponse('Payload Too Large', status=413)
	users = []
	if request.GET["type"] == "all":
		try:users = User.objects.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return HttpResponseNotFound()
	elif request.GET["type"] == "friends":
		try:
			if not request.GET["user"].isdigit():return HttpResponseBadRequest()
			users = User.objects.get(pk=request.GET["user"]).friends.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return HttpResponseNotFound()

	elif request.GET["type"] == "friends_and_want":
		try:
			if not request.GET["user"].isdigit():return HttpResponseBadRequest()
			users = request.user.friend_want_add.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
			if users.count()<20:
				users |= request.user.friends.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return HttpResponseNotFound()

	elif request.GET["type"] == "followers":
		try:
			if not request.GET["user"].isdigit():return HttpResponseBadRequest()
			users = User.objects.get(pk=request.GET["user"]).followers.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/users.html",{"users":users,"type":request.GET["type"]})

@login_required(login_url='login')
def saves_posts_ajax(request):
	try:
		# users = User.objects.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]
		posts = request.user.saves_posts.all()
	except:return HttpResponseNotFound()
	return render(request,"home/ajax_html/posts.html",{"posts":posts})

@login_required(login_url='login')
def music_get_ajax(request):
	if not request.GET["music_start"].isdigit() or not request.GET["music_end"].isdigit():return HttpResponseBadRequest()
	if int(request.GET["music_start"])-int(request.GET["music_end"])!=-20:return HttpResponse('Payload Too Large', status=413)

	try:music = Music.objects.all()[int(request.GET["music_start"]):int(request.GET["music_end"])]
	except: return HttpResponseNotFound()
	
	return render(request,"home/ajax_html/all_music.html",{"music":music,'type':"user_music_add"})

@login_required(login_url='login')
def music_find_ajax(request):
	if not request.GET["music_find_start"].isdigit() or not request.GET["music_find_end"].isdigit():return HttpResponseBadRequest()
	if int(request.GET["music_find_start"])-int(request.GET["music_find_end"])!=-20:return HttpResponse('Payload Too Large', status=413)

	try:music = Music.objects.filter(name__contains=request.GET["find_name"])[int(request.GET["music_find_start"]):int(request.GET["music_find_end"])]
	except:return HttpResponseNotFound()
	
	return render(request,"home/ajax_html/all_music.html",{"music":music,'type':"user_music_add"})

def video_get_ajax(request):
	return JsonResponse({"data":"while not functions"})
def video_find_ajax(request):
	return JsonResponse({"data":"while not functions"})

@login_required(login_url='login')
def playlists_ajax(request):
	playlists = request.user.playlists
	
	return render(request,"home/ajax_html/playlists.html",{"playlists":playlists})

@login_required(login_url='login')
def share_ch_ajax(request):
	if request.GET["type"] == 'find_ch':chats = request.user.chats.all().filter(Q(users__username__contains=request.GET["find_ch"])&~Q(users=request.user))
	else:chats = request.user.chats.all()
	return render(request,"home/ajax_html/share_ch.html",{"chats":chats})
