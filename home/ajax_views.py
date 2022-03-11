from django.shortcuts import render, redirect
from .models import User,Post,Chat,Comment,Theme,TypeMes,Playlist
from .forms import ThemeForm,MessageForm,AllTheme
from django.http import JsonResponse
from ameneuro.settings import get_posts_how, get_mes_how, get_user_how
from django.db.models import Q
from .services import *

from django.core import serializers

# in all need defence

def comment_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		try:post = Post.objects.get(pk=int(request.GET["id"]))
		except:return JsonResponse({"data_text":"Fail"}, status=400)

		return render(request,"home/ajax_html/comments.html",{"post_id":post.id ,"comments":post.comments.all()})
	return JsonResponse({"data_text":"Fail"}, status=400)

def post_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	posts = {}
	if request.GET["id"]:posts = Post.objects.filter(pk=request.GET["id"])
	else:posts = get_posts(request,user)

	if not posts:return JsonResponse({"info":"None post"}, status=200)
	return render(request, "home/ajax_html/posts.html",{"posts":posts})

def chat_options_ajax(request):
	user = {}
	chat = {}
	if request.user.is_authenticated:
		user = request.user
		try:chat = Chat.objects.get(pk=int(request.GET['chat_id']))
		except:return JsonResponse({"data_text":"Fail"}, status=400)

	form = ThemeForm()

	return render(request, "home/ajax_html/chat_options.html",{
			"user":user,
			"chat":chat,
			"form":form
		})

def chat_get_mess_ajax(request):
	user = {}
	chat = {}
	mess = {}
	if request.user.is_authenticated:
		user = request.user
		try:
			chat = Chat.objects.get(pk=int(request.GET['chat_id']))
			if not user in chat.users.all():return JsonResponse({"data_text":"Fail"}, status=400)
			mess = list(chat.messages.order_by('-date')[request.session['end_mes_wath']:request.session['end_mes_wath']+get_mes_how][::-1])
		except:return JsonResponse({"data_text":"Fail"}, status=400)
	else:return JsonResponse({"data_text":"Fail"}, status=400)

	request.session['end_mes_wath'] += get_mes_how

	return render(request, "home/ajax_html/mess.html",{"mess":mess})

def send_file_mes_ajax(request):
	form = MessageForm()
	error = ""
	if request.user.is_authenticated:
		user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	if request.method == "POST":
		src = ""
		form = MessageForm(request.POST, request.FILES)
		if form.is_valid():
			mes = form.save()
			mes.user = user
			mes.type_m = TypeMes.objects.get(type_m="file")
			mes.save()
			src = "/stream_mess/"+str(mes.id)
			chat = Chat.objects.get(pk=int(request.POST["chat_id"]))
			chat.messages.add(mes)
		else:
			return JsonResponse({"data_text":"Fail"}, status=400)
		return JsonResponse({"data_text":"OK","src":src,"type_file":mes.type_file.type_f,"id":mes.id}, status=200)

	return render(request,"home/ajax_html/send_file.html",{"form":form})

def musics_all_ajax(request):
	mus = {}
	if request.GET["type"] == "music_share":
		mus = request.user.music_shared
	elif request.GET["type"] == "playlist":
		mus = Playlist.objects.get(name=request.GET["ps"]).musics
	else:
		mus = request.user.music
	return render(request,"home/ajax_html/all_music.html",{"music":mus,'type':request.GET["type"]})

def user_find_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	try:
		users = User.objects.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	return render(request,"home/ajax_html/users.html",{"users":users})

def users_get_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)

	if int(request.GET["users_start"])-int(request.GET["users_end"])!=-20:
		return JsonResponse({"data_text":"Fail"}, status=400)

	if request.GET["type"] == "all":
		try:users = User.objects.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return JsonResponse({"data_text":"Fail"}, status=400)
	elif request.GET["type"] == "friends":
		try:users = User.objects.get(pk=request.GET["user"]).friends.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return JsonResponse({"data_text":"Fail"}, status=400)
	elif request.GET["type"] == "followers":
		try:users = User.objects.get(pk=request.GET["user"]).followers.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
		except:return JsonResponse({"data_text":"Fail"}, status=400)


	return render(request,"home/ajax_html/users.html",{"users":users,"type":request.GET["type"]})

def saves_posts_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	try:
		# users = User.objects.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]
		posts = user.saves_posts.all()
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	return render(request,"home/ajax_html/posts.html",{"posts":posts})

def music_get_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	if int(request.GET["music_start"])-int(request.GET["music_end"])!=-20:
		return JsonResponse({"data_text":"Fail"}, status=400)

	try:music = Music.objects.all()[int(request.GET["music_start"]):int(request.GET["music_end"])]
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	
	return render(request,"home/ajax_html/all_music.html",{"music":music,'type':"user_music_add"})

def music_find_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	# try:
	music = Music.objects.filter(name__contains=request.GET["find_name"])[int(request.GET["music_find_start"]):int(request.GET["music_find_end"])]
	# except:return JsonResponse({"data_text":"Fail"}, status=400)
	return render(request,"home/ajax_html/all_music.html",{"music":music,'type':"user_music_add"})

def video_get_ajax(request):
	return JsonResponse({"data":"while not functions"})
def video_find_ajax(request):
	return JsonResponse({"data":"while not functions"})

def playlists_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	playlists = request.user.playlists
	return render(request,"home/ajax_html/playlists.html",{"playlists":playlists})

def share_ch_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	if request.GET["type"] == 'find_ch':
		chats = user.chats.all().filter(Q(users__username__contains=request.GET["find_ch"])&~Q(users=user))
	else:
		chats = user.chats.all
	return render(request,"home/ajax_html/share_ch.html",{"chats":chats})
