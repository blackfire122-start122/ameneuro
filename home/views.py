from django.shortcuts import render, redirect
from .models import User,Post,Chat,Theme,AllTheme
from .forms import (RegisterForm,
					LoginForm,
					PostForm,
					ChangeForm,
					ThemeForm,
					MusicForm,
					AllThemeForm)
from django.contrib.auth import login, authenticate, logout
from django.http import StreamingHttpResponse
from django.views.generic import ListView, TemplateView, CreateView
from ameneuro.settings import get_posts_how, get_mes_how, get_user_how

from .services import *

class home(TemplateView):
	template_name = "home/home.html"
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			user = request.user
			request.session["start_element"] = 0
			request.session["end_element"] = get_posts_how
			request.session["end_post_friend"] = None
			request.session["start_rec_post"] = 0
			request.session["end_rec_post"] = get_posts_how
			request.session["start_rec_user"] = 0
			request.session["end_rec_user"] = get_user_how
			request.session["defolt_posts"] = False

			self.chat_not_read_count = 0
			for i in user.chats.all():
				if not i.messages.last().readeble and i.messages.last().user != user:
					self.chat_not_read_count+=1

		else:return redirect("login")
		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["chat_not_read_count"] = self.chat_not_read_count
		return context

class user(ListView):
	model = Post
	context_object_name = "posts"
	template_name = "home/user.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		self.user_reg = request.user

		try:self.user = User.objects.get(username=self.kwargs["name"])
		except:return redirect('home')

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["user"] = self.user
		context["user_reg"] = self.user_reg
		return context

	def get_queryset(self):
		# не брати всі
		return Post.objects.filter(user_pub=self.user.id).order_by("-date")

class chats(TemplateView):
	template_name = "home/chats.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		return super().get(request,*args, **kwargs)

class chat(TemplateView):
	template_name = "home/chat.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		
		try:self.chat = Chat.objects.get(chat_id=self.kwargs["chat_id"])
		except:return redirect("home")
		
		self.error = ""
		request.session['end_mes_wath'] = 0
		return super().get(request,*args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		
		try:self.chat = Chat.objects.get(chat_id=self.kwargs["chat_id"])
		except:return redirect("home")
		
		self.error = ""

		how_save = 0

		if request.POST['how_save']=='Save changes':
			form = ThemeForm(request.POST,request.FILES,instance=self.chat.theme)
			how_save = 0
		elif request.POST['how_save']=='Save theme':
			form = ThemeForm(request.POST,request.FILES)
			how_save = 1

		if form.is_valid():
			if how_save:
				theme = form.save()
				try:
					request.user.themes.add(theme.id)
					self.chat.theme = theme
					self.chat.save()
				except:error = 'save error'
			else:form.save()
		else:self.error = form.errors

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["chat"] = self.chat
		context["end_mes"] = self.chat.messages.last()
		context["error"] = self.error
		return context

class user_find(ListView):
	model = User
	context_object_name = "users"
	template_name = "home/user_find.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def get_queryset(self):
		# не брати всі
		return User.objects.all()

def login_user(request):
	error = ""
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(request.POST)
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user:
			login(request, user)
			return redirect("home")
		else:error = form.errors
	return render(request, "home/login.html",{'form':form,"error":error})

def sigin_user(request):
	form = RegisterForm()
	error = ""
	if request.method == "POST":		
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("home")
		else:error = form.errors
	return render(request, "home/sigin.html", {'form':form,"error":error})
	
def friends(request):
	user = {}
	user_friends_not_chat = {}
	if request.user.is_authenticated:
		user = request.user
		user_friends_not_chat = list(user.friends.all())
		# user_friends = user.friends.all()
	else:return redirect("login")

	user_friends_not_chat = del_friends(user_friends_not_chat,user)

	return render(request,"home/friends.html",{
		"user":user,
		"user_friends_not_chat":user_friends_not_chat
		})

def post(request,id):return render(request, "home/post.html",{"id":id})

def add_post(request):
	user = {}
	error = ""

	if request.user.is_authenticated:
		user = request.user
	else:return redirect("login")

	form = PostForm()

	if request.method=="POST":
		post_data = request.POST.copy()
		post_data["user_pub"]=user.id

		form = PostForm(post_data,request.FILES)
		if form.is_valid():
			form.save(user)
			return redirect('user',user.username)
		else:error = form.errors

	return render(request, "home/add_post.html",{"form":form,"error":error})

def streaming_post(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'post')
	response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range
	return response

def user_change(request):
	user = {}
	error = ''
	if request.user.is_authenticated:user = request.user
	else:return redirect("login")

	form_user = ChangeForm(instance=user)
	form_theme = AllThemeForm(instance=user.theme_all)

	default_themes = AllTheme.objects.filter(default=True)

	if request.method == 'POST':
		if request.POST['submit'] == 'Save changes':
			form_user = ChangeForm(request.POST,request.FILES,instance=user)
			if form_user.is_valid():
				form_user.save()
			else:
				error = form_user.errors
		elif request.POST['submit'] == 'Exit':
			logout(request)
			return redirect('login')

		elif request.POST['submit'] == 'Save changes theme':
			if user.theme_all.default:
				new_theme = user.theme_all
				new_theme.pk = None
				new_theme.default = False
				new_theme.save()
				user.theme_all = new_theme
			form_theme = AllThemeForm(request.POST,request.FILES,instance=user.theme_all)
			if form_theme.is_valid():
				user.theme_all = form_theme.save()
				user.save()
			else:error = form_theme.errors


	return render(request, "home/user_change.html",{
		"user":user,
		"form_user":form_user,
		"form_theme":form_theme,
		"default_themes":default_themes,
		"error":error
	})

def musics_all(request):
	if request.user.is_authenticated:user = request.user
	else:return redirect("login")

	return render(request, "home/music_all.html",{
		"user":user,
	})

def streaming_music(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'music')
	response = StreamingHttpResponse(file, status=status_code, content_type='music/mp3')

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range

	return response

class add_music(CreateView):
	template_name = 'home/add_music.html'
	form_class = MusicForm

	def form_valid(self, form):
		if self.request.user.is_authenticated:user = self.request.user
		else:return redirect("login")
		user.music.add(form.save())
		return redirect('musics')

def streaming_mess(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'mess')
	response = StreamingHttpResponse(file, status=status_code)

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range

	return response