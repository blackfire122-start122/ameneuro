from django.shortcuts import render, redirect
from .models import User,Post,Chat,Comment,Theme
from .forms import (RegisterForm,
					LoginForm,
					PostForm,
					ChangeForm,
					ThemeForm,
					MusicForm,
					MessageForm)
from django.contrib.auth import login, authenticate, logout
from django.http import (HttpResponseNotFound,
						JsonResponse,
						HttpResponseRedirect,
						HttpResponse,
						StreamingHttpResponse)
from django.views.generic import ListView, TemplateView, CreateView
from .services import *

get_posts_how = 5
get_mes_how = 20
get_user_how = 5

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
		else:return redirect("login")
		return super().get(request,*args, **kwargs)

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
		return Post.objects.filter(user_pub=self.user.id)

class chats(TemplateView):
	template_name = "home/chats.html"
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		return super().get(request,*args, **kwargs)

class chat(ListView):
	context_object_name = "messages"
	template_name = "home/chat.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		
		try:self.chat = Chat.objects.get(chat_id=self.kwargs["chat_id"])
		except:return redirect("home")
		
		self.error = ""
		request.session['end_mes_wath'] = get_mes_how
		return super().get(request,*args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:return redirect("login")
		
		try:self.chat = Chat.objects.get(chat_id=self.kwargs["chat_id"])
		except:return redirect("home")
		
		self.error = ""

		bg = request.POST['color_mes_bg'].lstrip('#')
		bg = ','.join([str(int(bg[i:i+2], 16)) for i in (0, 2, 4)])+','+request.POST['mes_bg_op']

		new_rp = request.POST.copy()
		new_rp['color_mes_bg'] = bg

		how_save = 0

		if request.POST['how_save']=='Save changes':
			form = ThemeForm(new_rp,request.FILES,instance=self.chat.theme)
			how_save = 0
		elif request.POST['how_save']=='Save theme':
			form = ThemeForm(new_rp,request.FILES)
			how_save = 1

		if form.is_valid():
			if how_save:
				theme = form.save()
				try:
					user.themes.add(theme.id)
					self.chat.theme = theme
					self.chat.save()
				except:error = 'save error'
			else:form.save()
		else:self.error = form.errors

		return super().get(request,*args, **kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		context["chat"] = self.chat
		context["error"] = self.error
		return context

	def get_queryset(self):
		#file неправильно
		return list(self.chat.messages.order_by('-date')[:get_mes_how][::-1])

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
	form = ChangeForm(instance=request.user)

	error = ''

	if request.user.is_authenticated:user = request.user
	else:return redirect("login")

	if request.method == 'POST':
		if request.POST['submit'] == 'Save changes':
			form = ChangeForm(request.POST,request.FILES,instance=request.user)
			if form.is_valid():
				form.save()
			else:
				error = form.errors
		elif request.POST['submit'] == 'Exit':
			logout(request)
			return redirect('login')

	return render(request, "home/user_change.html",{
		"user":user,
		"form":form,
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

# ajax

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
			
			theme = Theme(background='themes/default.jpg', color_mes='#FFFFFF',color_mes_bg='0,0,0,1',name=friend.username+user.username)
			theme.save()

			chat = Chat(chat_id=gen_rand_id(30))
			chat.theme=theme
			chat.save()

			chat.users.add(user.id)
			chat.users.add(friend.id)

			user.chats.add(chat.id)
			friend.chats.add(chat.id)
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
	# need recomendations and hard work

	posts = {}
	if request.GET["id"]:
		posts = Post.objects.filter(pk=request.GET["id"])
	else:
		if request.user.is_authenticated:
			user = request.user

			start = request.session["start_element"]
			end = request.session["end_element"]

			try:
				friends = user.friends.all()
				follow = user.follow.all()
				posts = Post.objects.filter(user_pub__in=friends|follow).order_by("-date")[start:end]
				if len(posts)<get_posts_how:
					start_rec_post = request.session["start_rec_post"]
					end_rec_post = request.session["end_rec_post"]

					start_rec_user = request.session["start_rec_user"]
					end_rec_user = request.session["end_rec_user"]

					rec_user = User.objects.exclude(pk__in=friends|follow)[start_rec_user:end_rec_user]
					posts |= Post.objects.filter(user_pub__in=rec_user).order_by("-date")[start_rec_post:end_rec_post]
				
					if request.session["defolt_posts"]:	
						start_rec_post = 0
						end_rec_post = get_posts_how
						request.session["defolt_posts"] = False

					if len(posts)<get_posts_how:
						request.session["defolt_posts"] = True

						start_rec_user+=get_user_how
						end_rec_user+=get_user_how

						request.session["start_rec_user"]=start_rec_user
						request.session["end_rec_user"]=end_rec_user
					
					start_rec_post+=get_posts_how
					end_rec_post+=get_posts_how

					request.session["start_rec_post"]=start_rec_post
					request.session["end_rec_post"]=end_rec_post

			except:return JsonResponse({"data_text":"Fail"}, status=400)

			start+=get_posts_how
			end+=get_posts_how

			request.session["start_element"]=start
			request.session["end_element"]=end
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
	else:
		return JsonResponse({"data_text":"Fail"}, status=400)

	if request.method == "POST":
		src = ""
		data_form = request.POST.copy()
		data_form['type_m'] = "file"
		form = MessageForm(data_form,request.FILES)
		if form.is_valid():
			mes = form.save()
			mes.user = user
			mes.save()
			src = mes.file.url
			chat = Chat.objects.get(pk=int(data_form["chat_id"]))
			chat.messages.add(mes)
		else:
			return JsonResponse({"data_text":"Fail"}, status=400)
		return JsonResponse({"data_text":"OK","src":src}, status=200)

	return render(request,"home/ajax_html/send_file.html",{"form":form})

def musics_all_ajax(request):
	user_mus = User.objects.get(pk = int(request.GET["id"]))
	return render(request,"home/ajax_html/all_music.html",{"music":user_mus.music})
