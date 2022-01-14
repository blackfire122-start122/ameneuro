from django.shortcuts import render, redirect
from .models import User,Post,Chat
from .forms import RegisterForm,LoginForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotFound,JsonResponse,HttpResponseRedirect,HttpResponse

import random
import string

strings = string.ascii_letters+string.digits

def home(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
	else:
		return redirect("login")

	# доробити пости не брати всі
	posts = Post.objects.all()

	return render(request, "home/home.html", {
		"user": user,
		"posts":posts
		})

def user(request,name):
	user = {}
	user_reg = {}
	posts = {}

	# user_reg = якщо зареєстрований
	if request.user.is_authenticated:
		user_reg = request.user

	user = User.objects.get(username=name)
	posts = Post.objects.filter(user_pub=user.id)

	return render(request, "home/user.html",{
		"user_reg":user_reg,
		"user":user,
		"posts":posts
	})

def chats(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
	else:
		return redirect("login")
	return render(request, "home/chats.html",{
			"user":user
		})

def chat(request,chat_id):
	user = {}
	chat = Chat.objects.get(chat_id=chat_id)
	messages = chat.messages.all().order_by("date")
	if request.user.is_authenticated:
		user = request.user
	return render(request, "home/chat.html",{
			"user":user,
			"messages":messages,
			"chat":chat
		})

def user_find(request):
	user = {}

	# доробити не брати всі

	users = User.objects.all()

	if request.user.is_authenticated:
		user = request.user

	return render(request, "home/user_find.html",{
			"user":user,
			"users":users
		})

def login_user(request):
	error = ""
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(request.POST)
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user:
			login(request, user)
			return redirect("home")
		else:
			error = "error"
	return render(request, "home/login.html",{'form':form,"error":error})

def sigin_user(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
	return render(request, "home/sigin.html", {'form':form})

def add_friend_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
		friend = User.objects.get(pk=int(request.GET["id"]))
		user.friends.add(friend)
		user.friend_want_add.remove(friend)

		return JsonResponse({"data_text":"OK"}, status=200)

	else:
		return JsonResponse({"data_text":"Fail"}, status=400)

def want_add_friend_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
		friend = User.objects.get(pk=int(request.GET["id"]))
		friend.friend_want_add.add(user)

		return JsonResponse({"data_text":"OK"}, status=200)

	else:
		return JsonResponse({"data_text":"Fail"}, status=400)


def del_friends(user_friends,user):
	for f in range(len(user_friends)):
		for fc in user_friends[f].chats.all():
			for uc in user.chats.all():
				if uc == fc:
					del user_friends[f]
					return del_friends(user_friends,user)
	return user_friends
	
def friends(request):
	user = {}
	user_friends = {}
	if request.user.is_authenticated:
		user = request.user
		user_friends = list(user.friends.all())
	else:
		return redirect("login")

	user_friends = del_friends(user_friends,user)

	return render(request,"home/friends.html",{
		"user":user,
		"user_friends":user_friends
		})

def gen_rand_id(n):
	res = ""
	for i in range(n):res+=random.choice(strings)
	return res

def add_chat_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		friend = User.objects.get(pk=int(request.GET["id"]))
		
		chat = Chat(chat_id=gen_rand_id(30))
		chat.save()

		chat.user.add(user)
		chat.user.add(friend)

		user.chats.add(chat)
		friend.chats.add(chat)

		return JsonResponse({"data_text":"OK"}, status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def like_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		post = Post.objects.get(pk=int(request.GET["id"]))
		post.likes.add(user)
		post.save()

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)
