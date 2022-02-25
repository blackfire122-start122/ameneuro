from django.shortcuts import render, redirect
from .models import User,Post,Chat,Comment,Theme,TypeMes
from .forms import ThemeForm,MessageForm,AllTheme
from django.http import JsonResponse
from ameneuro.settings import get_posts_how, get_mes_how, get_user_how

from .services import *

# in all need defence

def add_friend_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
		try:
			friend = User.objects.get(pk=int(request.GET["id"]))
			user.friends.add(friend.id)
			user.friend_want_add.remove(friend)
		except:return JsonResponse({"data_text":"Fail"}, status=400)
		
		return JsonResponse({"data_text":"OK"}, status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def want_add_friend_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
		try:
			friend = User.objects.get(pk=int(request.GET["id"]))
			friend.friend_want_add.add(user.id)
		except:return JsonResponse({"data_text":"Fail"}, status=400)
		
		return JsonResponse({"data_text":"OK"}, status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def add_chat_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		try:
			friend = User.objects.get(pk=int(request.GET["id"]))
			
			theme = Theme(background=None, color_mes='#FFFFFF',color_mes_bg='0,0,0,1',name=friend.username+user.username)
			theme.save()

			chat = Chat(chat_id=gen_rand_id(30))
			chat.theme=theme
			chat.save()

			chat.users.add(user.id)
			chat.users.add(friend.id)

			user.chats.add(chat.id)
			friend.chats.add(chat.id)

			user.themes.add(theme.id)
			friend.themes.add(theme.id)

		except:return JsonResponse({"data_text":"Fail"}, status=400)
		
		return JsonResponse({"url":"chat/"+chat.chat_id}, status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def like_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
		try:
			post = Post.objects.get(pk=int(request.GET["id"]))
			post.likes.add(user.id)
		except:return JsonResponse({"data_text":"Fail"}, status=400)

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		try:post = Post.objects.get(pk=int(request.GET["id"]))
		except:return JsonResponse({"data_text":"Fail"}, status=400)

		return render(request,"home/ajax_html/comments.html",{"post_id":post.id ,"comments":post.comments.all()})
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_like_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		try:
			com = Comment.objects.get(pk=int(request.GET["id"]))
			com.likes.add(user.id)
		except:return JsonResponse({"data_text":"Fail"}, status=400)

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_user_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		try:
			com = Comment(user=user,text=request.GET["text"])
			com.save()

			post = Post.objects.get(pk=int(request.GET["id"]))
			post.comments.add(com.id)

		except:return JsonResponse({"data_text":"Fail"}, status=400)

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_reply_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
		try:
			com = Comment(user=user,text=request.GET["text"])
			com.parent = Comment.objects.get(pk=int(request.GET["com_id"]))
			com.save()

			post = Post.objects.get(pk=int(request.GET["post_id"]))
			post.comments.add(com.id)
			return JsonResponse({"data_text":"OK"},status=200)
		except:
			return JsonResponse({"data_text":"Fail"}, status=400)
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

def follow_ajax(request):
	if request.user.is_authenticated:
		user = request.user
		try:
			follow_to = User.objects.get(pk=request.GET["id"])
			follow_to.followers.add(user.id)
			user.follow.add(follow_to.id)
		except:return JsonResponse({"data_text":"Fail"}, status=400)
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	return JsonResponse({"data_text":"OK"}, status=200)

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
		mus = User.objects.get(pk = int(request.GET["id"])).music_shared
	else:
		mus = User.objects.get(pk = int(request.GET["id"])).music
	return render(request,"home/ajax_html/all_music.html",{"music":mus,'type':request.GET["type"]})

def delete_post_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	try:post = Post.objects.get(pk=request.GET["id"])
	except:return JsonResponse({"data_text":"Fail"}, status=400)

	if post.user_pub == user:post.delete()
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	
	return JsonResponse({"data_text":"OK"}, status=200)

from django.core import serializers

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

	try:users = User.objects.all()[int(request.GET["users_start"]):int(request.GET["users_end"])]
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	
	return render(request,"home/ajax_html/users.html",{"users":users})

def new_theme_all_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)

	try:
		user.theme_all = AllTheme.objects.get(pk = int(request.GET["id"]))
		user.save()
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	
	return JsonResponse({"data_text":"OK"}, status=200)

def delete_theme_all_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)

	try:
		theme_del = AllTheme.objects.get(pk = int(request.GET["id"]))
		if not theme_del.default:theme_del.delete()
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	
	return JsonResponse({"data_text":"OK"}, status=200)

def saves_posts_ajax(request):
	if request.user.is_authenticated:user = request.user
	else:return JsonResponse({"data_text":"Fail"}, status=400)
	try:
		# users = User.objects.filter(username__contains=request.GET["find_name"])[int(request.GET["users_find_start"]):int(request.GET["users_find_end"])]
		posts = user.saves_posts.all()
	except:return JsonResponse({"data_text":"Fail"}, status=400)
	return render(request,"home/ajax_html/posts.html",{"posts":posts})
