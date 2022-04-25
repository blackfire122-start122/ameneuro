from django.shortcuts import render, redirect
from .models import User,Post,Chat,Comment,Theme,TypeMes,Playlist,Video
from .forms import ThemeForm,MessageForm,AllTheme
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .services import *

from django.core import serializers

@login_required(login_url='login')
def comment_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("id")):return HttpResponseBadRequest()
	except:return HttpResponseBadRequest()

	try:post = Post.objects.get(pk=request.GET.get("id"))
	except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/comments.html",{"post_id":post.id ,"comments":post.comments.all()})

@login_required(login_url='login')
def comment_video_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("start_comments"),request.GET.get("end_comments"),request.GET.get("id")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("start_comments"),request.GET.get("end_comments")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:
		video = Video.objects.get(pk=request.GET.get("id"))
		comments = video.comments.all()[int(request.GET.get("start_comments")):int(request.GET.get("end_comments"))]
	except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/comments_video.html",{"video_id":video.id,"comments":comments})

def post_ajax(request):
	posts = {}
	if request.GET.get("id"):
		try:
			if not defence_isdigit(request.GET.get("id")):return HttpResponseBadRequest()
		except:return HttpResponseBadRequest()
		
		try:posts = Post.objects.filter(pk=request.GET.get("id"))
		except: HttpResponseNotFound()
	else:posts = get_posts(request,request.user)

	if not posts:return HttpResponse("None post", status=200)
	return render(request, "home/ajax_html/posts.html",{"posts":posts,"data_get":request.GET})

def video_ajax(request):
	try:videos = get_videos(request)
	except: return HttpResponseNotFound()

	if not videos:return HttpResponse("None video", status=200)
	return render(request, "home/ajax_html/videos.html",{"videos":videos,"data_get":request.GET})


@login_required(login_url='login')
def chat_options_ajax(request):
	chat = {}
	try:
		if not defence_isdigit(request.GET.get("chat_id")):return HttpResponseBadRequest()
	except:return HttpResponseBadRequest()

	try:chat = Chat.objects.get(pk=request.GET.get('chat_id'))
	except:return HttpResponseNotFound()

	if request.user != chat.user:return HttpResponseForbidden()

	form = ThemeForm()

	return render(request, "home/ajax_html/chat_options.html",{
			"chat":chat,
			"form":form
		})

@login_required(login_url='login')
def chat_get_mess_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("mess_start"),request.GET.get("mess_end"),request.GET.get("chat_id")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("mess_start"),request.GET.get("mess_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()
	mess = []

	try:chat = Chat.objects.get(pk=request.GET.get('chat_id'))
	except:return HttpResponseNotFound()

	if request.user != chat.user:return HttpResponseForbidden()
	mess = chat.messages.order_by('-date')[int(request.GET.get("mess_start")):int(request.GET.get("mess_end"))][::-1]

	return render(request, "home/ajax_html/mess.html",{"mess":mess})

@login_required(login_url='login')
def send_file_mes_ajax(request):
	form = MessageForm()
	error = ""

	if request.method == "POST":
		try:
			if not defence_isdigit(request.POST.get("chat_id")):return HttpResponseBadRequest()
		except:return HttpResponseBadRequest()
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
			chat.chat_friend.messages.add(mes)
		else:return HttpResponseBadRequest()
		return JsonResponse({"data_text":"OK","src":src,"type_file":mes.type_file.type_f,"id":mes.id}, status=200)

	return render(request,"home/ajax_html/send_file.html",{"form":form})

@login_required(login_url='login')
def musics_all_ajax(request):
	if request.GET.get("type") == "music_share":mus = request.user.music_shared
	elif request.GET.get("type") == "playlist":
		try:
			if not defence_isdigit(request.GET.get("musics_start"),request.GET.get("musics_end")):return HttpResponseBadRequest()
			if not defence_ptl(request.GET.get("musics_start"),request.GET.get("musics_end")):return HttpResponse('Payload Too Large', status=413)
		except:return HttpResponseBadRequest()

		try:mus = Playlist.objects.get(pk=request.GET.get("ps")).musics.all()[int(request.GET.get("musics_start")):int(request.GET.get("musics_end"))]
		except:return HttpResponseNotFound()

	elif request.GET.get("type") == "user_music_add":
		try:mus = User.objects.get(pk=request.GET.get("id")).music
		except:return HttpResponseNotFound()
	else:
		try:
			if not defence_isdigit(request.GET.get("musics_start"),request.GET.get("musics_end")):return HttpResponseBadRequest()
			if not defence_ptl(request.GET.get("musics_start"),request.GET.get("musics_end")):return HttpResponse('Payload Too Large', status=413)
		except:return HttpResponseBadRequest()

		mus = request.user.music.all()[int(request.GET.get("musics_start")):int(request.GET.get("musics_end"))]
	return render(request,"home/ajax_html/all_music.html",{"music":mus,"data_get":request.GET})

@login_required(login_url='login')
def user_find_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("users_find_start"), request.GET.get("users_find_end")):return HttpResponseBadRequest()
		if int(request.GET.get("users_find_end"))-int(request.GET.get("users_find_start"))!=20:return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()
	
	users = []
	if request.GET.get("type") == "all":
		try:
			users = User.objects.filter(username__contains=request.GET.get("find_name"))[int(request.GET.get("users_find_start")):int(request.GET.get("users_find_end"))]
		except:return HttpResponseNotFound()
	elif request.GET.get("type") == "friends_and_want":
		try:
			users = request.user.friend_want_add.filter(username__contains=request.GET.get("find_name"))[int(request.GET.get("users_find_start")):int(request.GET.get("users_find_end"))]
			if users.count()<20:
				users |= request.user.friends.filter(username__contains=request.GET.get("find_name"))[int(request.GET.get("users_find_start")):int(request.GET.get("users_find_end"))]

		except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/users.html",{"users":users,"type":request.GET.get("type")})

@login_required(login_url='login')
def users_get_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("users_start"),request.GET.get("users_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("users_start"),request.GET.get("users_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	users = []
	if request.GET.get("type") == "all":
		try:users = User.objects.all()[int(request.GET.get("users_start")):int(request.GET.get("users_end"))]
		except:return HttpResponseNotFound()
	elif request.GET.get("type") == "friends":
		try:
			if not request.GET.get("user"):return HttpResponseBadRequest()
			users = User.objects.get(pk=request.GET.get("user")).friends.all()[int(request.GET.get("users_start")):int(request.GET.get("users_end"))]
		except:return HttpResponseNotFound()

	elif request.GET.get("type") == "friends_and_want":
		try:
			users = request.user.friend_want_add.all()[int(request.GET.get("users_start")):int(request.GET.get("users_end"))]
			if users.count()<20:
				users |= request.user.friends.all()[int(request.GET.get("users_start")):int(request.GET.get("users_end"))]
		except:return HttpResponseNotFound()

	elif request.GET.get("type") == "followers":
		try:
			if not request.GET.get("user"):return HttpResponseBadRequest()
			users = User.objects.get(pk=request.GET.get("user")).followers.all()[int(request.GET.get("users_start")):int(request.GET.get("users_end"))]
		except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/users.html",{"users":users,"type":request.GET.get("type")})

@login_required(login_url='login')
def saves_posts_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("start_post"), request.GET.get("end_post")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("start_post"),request.GET.get("end_post")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:posts = request.user.saves_posts.all()[int(request.GET.get("start_post")):int(request.GET.get("end_post"))]
	except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/posts.html",{"posts":posts})

@login_required(login_url='login')
def music_get_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("music_start"), request.GET.get("music_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("music_start"),request.GET.get("music_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:music = Music.objects.all()[int(request.GET.get("music_start")):int(request.GET.get("music_end"))]
	except: return HttpResponseNotFound()
	
	if request.GET.get("type") == "music_select":
		try:ps = Playlist.objects.get(pk=request.GET.get("playlist_id"))
		except:return HttpResponseNotFound()
		return render(request,"home/ajax_html/all_music.html",{"music":music,"data_get":request.GET,'playlist':ps})

	return render(request,"home/ajax_html/all_music.html",{"music":music,"data_get":request.GET})

@login_required(login_url='login')
def music_find_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("music_find_start"), request.GET.get("music_find_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("music_find_start"),request.GET.get("music_find_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:music = Music.objects.filter(name__contains=request.GET.get("find_name"))[int(request.GET.get("music_find_start")):int(request.GET.get("music_find_end"))]
	except:return HttpResponseNotFound()

	if request.GET.get("type") == "music_select":
		try:ps = Playlist.objects.get(pk=request.GET.get("playlist_id"))
		except:return HttpResponseNotFound()
		return render(request,"home/ajax_html/all_music.html",{"music":music,"data_get":request.GET,'playlist':ps})

	return render(request,"home/ajax_html/all_music.html",{"music":music,"data_get":request.GET})

@login_required(login_url='login')
def playlist_get_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("playlist_start"), request.GET.get("playlist_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("playlist_start"),request.GET.get("playlist_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:ps = Playlist.objects.all()[int(request.GET.get("playlist_start")):int(request.GET.get("playlist_end"))]
	except: return HttpResponseNotFound()
	
	return render(request,"home/ajax_html/playlists.html",{"playlists":ps})

@login_required(login_url='login')
def playlist_find_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("playlist_find_start"), request.GET.get("playlist_find_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("playlist_find_start"),request.GET.get("playlist_find_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:ps = Playlist.objects.filter(name__contains=request.GET.get("find_name"))[int(request.GET.get("playlist_find_start")):int(request.GET.get("playlist_find_end"))]
	except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/playlists.html",{"playlists":ps})

def video_get_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("video_start"), request.GET.get("video_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("video_start"),request.GET.get("video_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:videos = Video.objects.all()[int(request.GET.get("video_start")):int(request.GET.get("video_end"))]
	except: return HttpResponseNotFound()
	
	return render(request,"home/ajax_html/videos.html",{"videos":videos})

def video_find_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("video_find_start"), request.GET.get("video_find_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("video_find_start"),request.GET.get("video_find_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:videos = Video.objects.filter(name__contains=request.GET.get("find_name"))[int(request.GET.get("video_find_start")):int(request.GET.get("video_find_end"))]
	except:return HttpResponseNotFound()

	return render(request,"home/ajax_html/videos.html",{"videos":videos})


@login_required(login_url='login')
def playlists_ajax(request):
	if request.GET.get("type") == "ps_share":playlists = request.user.playlists_shared
	else:
		try:
			if not defence_isdigit(request.GET.get("playlists_start"),request.GET.get("playlists_end")):return HttpResponseBadRequest()
			if not defence_ptl(request.GET.get("playlists_start"),request.GET.get("playlists_end")):return HttpResponse('Payload Too Large', status=413)
		except:return HttpResponseBadRequest()
		playlists = request.user.playlists.all()[int(request.GET.get("playlists_start")):int(request.GET.get("playlists_end"))]
	return render(request,"home/ajax_html/playlists.html",{"playlists":playlists,"data_get":request.GET})

@login_required(login_url='login')
def share_ch_ajax(request):
	if request.GET.get("type") == 'find_ch':chats = request.user.chats.all().filter(Q(user__username__contains=request.GET.get("find_ch"))&~Q(users=request.user))
	else:chats = request.user.chats.all()
	return render(request,"home/ajax_html/share_ch.html",{"chats":chats})

def post_user_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("posts_start"), request.GET.get("posts_end"), request.GET.get("user")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("posts_start"),request.GET.get("posts_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:posts = Post.objects.filter(user_pub=request.GET.get("user")).order_by("-date")[int(request.GET.get("posts_start")):int(request.GET.get("posts_end"))]
	except:return HttpResponseNotFound()
	return render(request,"home/ajax_html/post_user.html",{"posts":posts})

def video_user_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("videos_start"), request.GET.get("videos_end"), request.GET.get("user")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("videos_start"),request.GET.get("videos_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()

	try:videos = Video.objects.filter(user_pub=request.GET.get("user")).order_by("-date")[int(request.GET.get("videos_start")):int(request.GET.get("videos_end"))]
	except:return HttpResponseNotFound()
	return render(request,"home/ajax_html/video_user.html",{"videos":videos})

@login_required(login_url='login')
def activity_mess_ajax(request):
	try:
		if not defence_isdigit(request.GET.get("mess_start"), request.GET.get("mess_end")):return HttpResponseBadRequest()
		if not defence_ptl(request.GET.get("mess_start"),request.GET.get("mess_end")):return HttpResponse('Payload Too Large', status=413)
	except:return HttpResponseBadRequest()
	
	try:mess = request.user.message_activity.all().order_by("-date")[int(request.GET.get('mess_start')):int(request.GET.get('mess_end'))]
	except:return HttpResponseNotFound()
	return render(request, "home/ajax_html/activity_mess.html",{"mess":mess})