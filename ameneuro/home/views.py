from django.shortcuts import render, redirect
from .models import User,Post,Chat
from .forms import RegisterForm,LoginForm
from django.contrib.auth import login, authenticate

def home(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

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
	return render(request, "home/chats.html",{
			"user":user
		})

def chat(request,chat_id):
	user = {}
	chat = Chat.objects.get(chat_id=chat_id)
	if request.user.is_authenticated:
		user = request.user
	return render(request, "home/chat.html",{
			"user":user,
			"chat":chat
		})

def user_find(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
	return render(request, "home/user_find.html",{
			"user":user
		})

def login_user(request):
	error = ""
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(request.POST)
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user:
			login(request, user)
			redirect("home")
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
