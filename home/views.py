from django.shortcuts import render, redirect
from .models import User,Post,Chat,Comment
from .forms import RegisterForm,LoginForm,PostForm
from django.contrib.auth import login, authenticate
from django.http import (HttpResponseNotFound,
						JsonResponse,
						HttpResponseRedirect,
						HttpResponse,
						StreamingHttpResponse)

from .services import *

def home(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user
	else:
		return redirect("login")

	return render(request, "home/home.html", {
		"user": user,
		})

def user(request,name):
	user = {}
	user_reg = {}
	posts = {}

	if request.user.is_authenticated:
		user_reg = request.user

	try:
		user = User.objects.get(username=name)
		posts = Post.objects.filter(user_pub=user.id)
	except:
		return redirect("home")
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
	if request.user.is_authenticated:
		user = request.user

	try:
		chat = Chat.objects.get(chat_id=chat_id)
		messages = chat.messages.all().order_by("date")
	except:
		return redirect("home")

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

def post(request,id):
	return render(request, "home/post.html",{"id":id})

def add_post(request):
	user = {}
	error = ""

	if request.user.is_authenticated:
		user = request.user
	else:
		return redirect("login")

	form = PostForm()

	if request.method=="POST":
		post_data = request.POST.copy()
		post_data["user_pub"]=user.id

		form = PostForm(post_data,request.FILES)
		if form.is_valid():
			form.save(user)
			return redirect('user',user.username)
		else:
			error = form.errors

	return render(request, "home/add_post.html",{"form":form,"error":error})

def streaming_post(request,id):
    file, status_code, content_length, content_range = open_file(request,id)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

# ajax

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

def add_chat_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		friend = User.objects.get(pk=int(request.GET["id"]))
		
		chat = Chat(chat_id=gen_rand_id(30))
		chat.save()

		chat.users.add(user)
		chat.users.add(friend)

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

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		post = Post.objects.get(pk=int(request.GET["id"]))

		return render(request,"home/ajax_html/comments.html",{"post_id":post.id ,"comments":post.comments.all()})
	return JsonResponse({"data_text":"Fail"}, status=400)


def comment_like_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		com = Comment.objects.get(pk=int(request.GET["id"]))
		com.likes.add(user)

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_user_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		com = Comment(user=user,text=request.GET["text"])
		com.save()

		post = Post.objects.get(pk=int(request.GET["id"]))
		post.comments.add(com)

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def comment_reply_ajax(request):
	user = {}
	if request.user.is_authenticated:
		user = request.user

		com = Comment(user=user,text=request.GET["text"])
		com.parent = Comment.objects.get(pk=int(request.GET["com_id"]))
		com.save()

		post = Post.objects.get(pk=int(request.GET["post_id"]))
		post.comments.add(com)

		return JsonResponse({"data_text":"OK"},status=200)
	return JsonResponse({"data_text":"Fail"}, status=400)

def post_ajax(request):
	if request.GET["id"]:
		posts = Post.objects.filter(pk=request.GET["id"])
	else:
		posts = Post.objects.all()
	return render(request, "home/ajax_html/posts.html",{"posts":posts.all()})
