from django.shortcuts import render, redirect
from .models import User,Post,Chat,Theme,AllTheme,Playlist
from .forms import (RegisterForm,
					LoginForm,
					PostForm,
					ChangeForm,
					ThemeForm,
					MusicForm,
					AllThemeForm,
					PlaylistForm)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import ListView, TemplateView, CreateView
from ameneuro.settings import get_posts_how, get_mes_how, get_user_how

from .services import *

class home(LoginRequiredMixin,TemplateView):
	template_name = "home/home.html"
	login_url = 'login'

	def get(self, request, *args, **kwargs):
		request.session["start_element"] = 0
		request.session["end_element"] = get_posts_how
		request.session["end_post_friend"] = None
		request.session["start_rec_post"] = 0
		request.session["end_rec_post"] = get_posts_how
		request.session["start_rec_user"] = 0
		request.session["end_rec_user"] = get_user_how
		request.session["defolt_posts"] = False

		request.session["start_element_video"] = 0
		request.session["end_element_video"] = get_posts_how
		request.session["end_video_friend"] = None
		request.session["start_rec_video"] = 0
		request.session["end_rec_video"] = get_posts_how
		request.session["start_rec_video_user"] = 0
		request.session["end_rec_video_user"] = get_user_how
		request.session["defolt_video"] = False

		
		self.chat_not_read_count = 0
		for i in request.user.chats.all():
			if i.messages.last() and not i.messages.last().readeble and i.messages.last().user != request.user:
				self.chat_not_read_count+=1

		self.music_shared = request.user.music_shared.count()
		self.message_activity = request.user.message_activity.filter(readeble=False).count()

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["chat_not_read_count"] = self.chat_not_read_count
		context["music_shared"] = self.music_shared
		context["message_activity"] = self.message_activity
		return context

class user(TemplateView):
	template_name = "home/user.html"

	def get(self, request, *args, **kwargs):
		self.user_reg = request.user

		try:self.user = User.objects.get(username=self.kwargs["name"])
		except:return HttpResponseNotFound()

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["user"] = self.user
		context["user_reg"] = self.user_reg
		return context

class chats(LoginRequiredMixin,TemplateView):
	template_name = "home/chats.html"
	login_url = 'login'

class chat(LoginRequiredMixin,TemplateView):
	template_name = "home/chat.html"
	login_url = 'login'

	def get(self, request, *args, **kwargs):
		try:self.chat = Chat.objects.get(chat_id=self.kwargs["chat_id"])
		except:return HttpResponseNotFound()
		
		self.error = ""
		request.session['end_mes_wath'] = 0
		return super().get(request,*args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		try:self.chat = Chat.objects.get(chat_id=self.kwargs["chat_id"])
		except:return HttpResponseNotFound()
		
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

class find(LoginRequiredMixin,TemplateView):
	template_name = "home/find.html"
	login_url = 'login'

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

class friends(LoginRequiredMixin, TemplateView):
	template_name = "home/friends.html"
	login_url = 'login'

def post(request,id):return render(request, "home/post.html",{"id":id})
def video(request,name):
	try:video = Video.objects.get(name=name)
	except:return HttpResponseNotFound()
	return render(request, "home/video.html",{"video":video})

class add_post(LoginRequiredMixin,TemplateView):
	template_name = "home/add_post.html"
	login_url = "login"

	def get(self, request, *args, **kwargs):
		self.form = PostForm()
		self.error = ''
		return super().get(request,*args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		self.error = ''
		post_data = request.POST.copy()
		post_data["user_pub"]=request.user.id

		self.form = PostForm(post_data,request.FILES)
		if self.form.is_valid():
			self.form.save(request.user)
			return redirect('user',request.user.username)
		else:error = self.form.errors

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["form"] = self.form
		context["error"] = self.error
		return context

def stream_video(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'video')
	response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range
	return response

def streaming_post(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'post')
	response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range
	return response

class user_change(LoginRequiredMixin,TemplateView):
	template_name = "home/user_change.html"
	login_url = "login"

	def get(self, request, *args, **kwargs):
		self.form_user = ChangeForm(instance=request.user)
		self.form_theme = AllThemeForm(instance=request.user.theme_all)
		self.default_themes = AllTheme.objects.filter(default=True)
		self.error = ''

		return super().get(request,*args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.form_user = ChangeForm(instance=request.user)
		self.form_theme = AllThemeForm(instance=request.user.theme_all)
		self.default_themes = AllTheme.objects.filter(default=True)
		self.error = ''

		if request.POST['submit'] == 'Save changes':
			self.form_user = ChangeForm(request.POST,request.FILES,instance=request.user)
			if self.form_user.is_valid():
				self.form_user.save()
			else:
				self.error = self.form_user.errors
		elif request.POST['submit'] == 'Exit':
			logout(request)
			return redirect('login')

		elif request.POST['submit'] == 'Save changes theme' or 'Save new theme':
			if request.user.theme_all.default or request.POST['submit'] == 'Save new theme':
				new_theme = request.user.theme_all
				new_theme.pk = None
				new_theme.default = False
				new_theme.save()
				request.user.theme_all = new_theme
			self.form_theme = AllThemeForm(request.POST,request.FILES,instance=request.user.theme_all)
			if self.form_theme.is_valid():
				theme_all_update = self.form_theme.save()
				request.user.theme_all = theme_all_update
				request.user.themes_all.add(theme_all_update)
				request.user.save()
			else:self.error = self.form_theme.errors
		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["form_user"]= self.form_user
		context["form_theme"]= self.form_theme
		context["default_themes"]= self.default_themes
		context["error"]= self.error

		return context

class musics_all(LoginRequiredMixin,TemplateView):
	template_name = "home/music_all.html"
	login_url = "login"

def streaming_music(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'music')
	response = StreamingHttpResponse(file, status=status_code, content_type='music/mp3')

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range

	return response

class add_music(LoginRequiredMixin,CreateView):
	template_name = 'home/add_music.html'
	form_class = MusicForm
	login_url = "login"

	def form_valid(self, form):
		self.request.user.music.add(form.save())
		return redirect('musics')

def streaming_mess(request,id):
	file, status_code, content_length, content_range = open_file(request,id,'mess')
	response = StreamingHttpResponse(file, status=status_code)

	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(content_length)
	response['Cache-Control'] = 'no-cache'
	response['Content-Range'] = content_range

	return response

class saves_posts(LoginRequiredMixin,TemplateView):
	template_name = "home/save_posts.html"
	login_url = "login"

class playlists(LoginRequiredMixin,TemplateView):
	template_name = "home/playlists.html"
	login_url = "login"

	def get(self, request, *args, **kwargs):
		try:self.ps = Playlist.objects.get(name=self.kwargs["name"])
		except: return HttpResponseNotFound()

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["playlist"] = self.ps
		return context

class activity(LoginRequiredMixin,TemplateView):
	template_name = "home/activity.html"
	login_url = "login"

class add_playlist(LoginRequiredMixin,TemplateView):
	template_name = "home/add_playlist.html"
	login_url = "login"

	def get(self, request, *args, **kwargs):
		self.form = PlaylistForm()
		self.error = ''
		return super().get(request,*args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		self.error = ''
		post_data = request.POST.copy()
		post_data["autor"]=request.user.id
		
		self.form = PlaylistForm(post_data,request.FILES)
		if self.form.is_valid():
			request.user.playlists.add(self.form.save(request.user))
			return redirect('change_playlist',post_data['name'])
		else:error = self.form.errors

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["form"] = self.form
		context["error"] = self.error
		return context

class change_playlist(LoginRequiredMixin,TemplateView):
	template_name = "home/change_playlist.html"
	login_url = "login"

	def get(self, request, *args, **kwargs):
		self.playlist = Playlist.objects.get(name=self.kwargs["name"])
		if request.user != self.playlist.autor:
			return HttpResponseBadRequest()
		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context